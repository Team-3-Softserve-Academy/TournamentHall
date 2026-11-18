# Database Configuration & Initialization

This document explains the requirements, connection parameters, and execution process for initializing the database using `init_db.sh` (on the DB VM) and creating the schema using `configure_db.sh` / `models.py` (on the App VM). It also covers essential database-level security configurations.

## 1. Core Prerequisites

SQLAlchemy's initialization process (`Base.metadata.create_all`) only creates **tables** inside an existing database. It cannot create the database itself or manage PostgreSQL roles. Before running the Python script, the following must exist on the target machine:

1. **Running DBMS**: An active PostgreSQL server instance listening for connections.
2. **Database Role (User)**: A dedicated PostgreSQL user with password authentication and privileges to create tables.
3. **Target Database**: An empty database owned by (or accessible to) the created user.

*Example of creating a user and database via terminal (Ubuntu/PostgreSQL):*
```bash
sudo -u postgres psql -c "CREATE USER postgresql WITH PASSWORD 'postgresql';"
sudo -u postgres psql -c "CREATE DATABASE tournament_db OWNER postgresql;"
```

## 2. Required Python Packages

The database layer relies on three packages that must be installed in your virtual environment (`venv`).

* **`SQLAlchemy`**: The ORM used to map Python classes (`Lord`, `Knight`, `CommonFolk`) to database tables.
* **`psycopg2-binary`** (or **`psycopg[binary]`**): The low-level PostgreSQL database adapter (driver).
* **`python-dotenv`**: Reads key-value pairs from a local `.env` file.

To install these dependencies, ensure your virtual environment is active and execute:
```bash
pip install SQLAlchemy psycopg2-binary python-dotenv
```

## 3. Connection URI & Environment Variables

`database_access.py` builds the SQLAlchemy connection URI from the environment variables in `.env` (or `.env.example` if `.env` is absent).

### URI Format
```
dialect+driver://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME
```

### Parameter Breakdown

| Variable / Parameter | Purpose | Example Value |
| :--- | :--- | :--- |
| **`dialect+driver`** | Defines the database type and Python driver. | `postgresql+psycopg2` |
| **`DB_USER`** | The PostgreSQL role used to authenticate. | `postgresql` |
| **`DB_PASSWORD`** | The password for the specified PostgreSQL role. | `postgresql` |
| **`DB_HOST`** | The private IP address of the PostgreSQL DB VM. | `192.168.56.64` |
| **`DB_PORT`** | The TCP port the PostgreSQL server listens on. | `5432` |
| **`DB_NAME`** | The target database name. | `tournament_db` |
| **`ALLOWED_IPS`** | Space-separated list of App VM IPs allowed in `pg_hba.conf`. | `"192.168.56.16 192.168.56.32"` |

### Example `.env` / `.env.example`
```env
DB_USER=postgresql
DB_PASSWORD=postgresql
DB_HOST=192.168.56.64
DB_PORT=5432
DB_NAME=tournament_db

# Application server IPs allowed to connect to PostgreSQL (space-separated)
ALLOWED_IPS="192.168.56.16 192.168.56.32"
```
*(resulting URI: `postgresql+psycopg2://postgresql:postgresql@192.168.56.64:5432/tournament_db`)*

## 4. Schema Initialization (`models.py`)

`models.py` defines the ORM models and creates the corresponding tables and constraints in PostgreSQL:

* **`Lord` (`lords`)**: Stores lord records (`name` up to 100 chars, `image_url` string, `house` up to 100 chars).
* **`Knight` (`knights`)**: Stores knight records (`name` and `house` up to 100 chars, `image_url` string, combat stats `strength`, `speed`, and `protection` constrained between `1` and `20`, unique `key` up to 255 chars, and `key_last_used` timestamp).
* **`CommonFolk` (`commonfolks`)**: Stores common folk records (`name` up to 100 chars).

### How It Works
1. Imports `engine` and `Base` from `database_access.py` (which automatically reads `.env` or falls back to `.env.example`).
2. Registers the `Lord`, `Knight`, and `CommonFolk` table structures and `CheckConstraint` rules in `Base.metadata`.
3. Executes `Base.metadata.create_all(bind=engine)`, which issues `CREATE TABLE IF NOT EXISTS` statements to the database.

Run the script once after configuring `.env` to create the schema:
```bash
python3 models.py
```

## 5. Security & Access Control Hardening

Relying solely on OS-level firewalls (like UFW) is not enough. The database itself must enforce strict access rules. Run these commands on the **DB Node** to secure the PostgreSQL instance.

*(Note: Replace `192.168.50.14` with your DB Node IP, and `192.168.50.10` with your App Node IP).*

**Step 1: Enforce Least Privilege and Connection Limits**
Restrict the application user so it cannot create other databases or roles, and limit concurrent connections to prevent resource exhaustion attacks.
```bash
sudo -u postgres psql -c "ALTER ROLE postgresql WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
```

**Step 2: Bind to Specific Network Interfaces**
Configure PostgreSQL to listen only on the local interface and the specific private IP of the DB node (`DB_HOST`, do not use `*`).
```bash
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, 192.168.56.64';"
```

**Step 3: Configure the Internal Firewall (`pg_hba.conf`)**
Allow connections to `tournament_db` as `postgresql` only from the specific App node IPs (`ALLOWED_IPS`) using `scram-sha-256`.
```bash
PG_HBA=$(sudo -u postgres psql -t -P format=unaligned -c 'show hba_file')
for IP in 192.168.56.16 192.168.56.32; do
    echo "host tournament_db postgresql ${IP}/32 scram-sha-256" | sudo tee -a "$PG_HBA"
done
```

**Step 4: Apply Changes**
Restart the PostgreSQL service to load the new network bindings and HBA rules.
```bash
sudo systemctl restart postgresql
```

## 6. Full End-to-End Setup Example

### Part A: On the DB VM (`init_db.sh`)
```bash
# 1. Install and start PostgreSQL service
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo systemctl start postgresql

# 2. Create the target database and restricted user
sudo -u postgres psql -c "CREATE USER postgresql WITH PASSWORD 'postgresql';"
sudo -u postgres psql -c "CREATE DATABASE tournament_db OWNER postgresql;"

# 3. Apply Security Hardening (Limits, Network bindings & pg_hba.conf)
sudo -u postgres psql -c "ALTER ROLE postgresql WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, 192.168.56.64';"
PG_HBA=$(sudo -u postgres psql -t -P format=unaligned -c 'show hba_file')
for IP in 192.168.56.16 192.168.56.32; do
    echo "host tournament_db postgresql ${IP}/32 scram-sha-256" | sudo tee -a "$PG_HBA"
done
sudo systemctl restart postgresql
```

### Part B: On the App VM (`configure_db.sh`)
```bash
# 1. Install Python environment tools
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip

# 2. Setup virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv

# 3. Initialize schema creating tables in the remote database
python3 models.py
```

### Automated Vagrant Setup (`init_db.sh` & `configure_db.sh`)
To automate provisioning in your `Vagrantfile`, run `init_db.sh` on the `database` VM and `configure_db.sh` on the application VM:
```ruby
database.vm.provision "shell", path: "init_db.sh"
app01.vm.provision "shell", path: "configure_db.sh"
```