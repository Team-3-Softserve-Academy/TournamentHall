# Database Configuration & Initialization

This document explains the requirements, connection parameters, and execution process for initializing the database schema using `models.py`, `database_access.py`, and the automated Vagrant provisioning script `init.sh`. It also covers essential database-level security configurations.

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
dialect+driver://DB_USER:DB_PASSWORD@127.0.0.1:DB_PORT/DB_NAME
```

### Parameter Breakdown

| Variable / Parameter | Purpose | Example Value |
| :--- | :--- | :--- |
| **`dialect+driver`** | Defines the database type and Python driver. | `postgresql` |
| **`DB_USER`** | The PostgreSQL role used to authenticate. | `postgresql` |
| **`DB_PASSWORD`** | The password for the specified PostgreSQL role. | `postgresql` |
| **`DB_PORT`** | The TCP port the PostgreSQL server listens on. | `5432` |
| **`DB_NAME`** | The target database name. | `tournament_db` |
| **`ALLOWED_IPS`** | Comma-separated list of IPs for `listen_addresses`. | `"192.168.50.10, 192.168.50.11"` |

### Example `.env` / `.env.example`
```env
DB_USER=postgresql
DB_PASSWORD=postgresql
DB_PORT=5432
DB_NAME=tournament_db

# Server IPs allowed to connect to PostgreSQL
# Example: ALLOWED_IPS="192.168.50.10, 192.168.50.11"
ALLOWED_IPS=
```
*(resulting URI: `postgresql://postgresql:postgresql@127.0.0.1:5432/tournament_db`)*

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
Configure PostgreSQL to listen only on the local interface and the specific private IP of the DB node (do not use `*`).
```bash
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, 192.168.50.14';"
```

**Step 3: Apply Changes**
Restart the PostgreSQL service to load the new network bindings.
```bash
sudo systemctl restart postgresql
```

## 6. Full End-to-End Setup Example

Here is a complete sequence of terminal commands to initialize and secure the database from scratch.

```bash
# 1. Start PostgreSQL service
sudo systemctl start postgresql

# 2. Create the target database and restricted user
sudo -u postgres psql -c "CREATE USER postgresql WITH PASSWORD 'postgresql';"
sudo -u postgres psql -c "CREATE DATABASE tournament_db OWNER postgresql;"

# 3. Apply Security Hardening (Limits & Network bindings)
sudo -u postgres psql -c "ALTER ROLE postgresql WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, 192.168.50.14';"
sudo systemctl restart postgresql

# 4. Setup Python Environment & Initialize Schema
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv
python3 models.py

# 5. Clean up temporary Python environment and packages
deactivate
rm -rf venv
sudo apt-get remove --purge -y python3-venv python3-pip
sudo apt-get autoremove -y
```

### Automated Vagrant Setup (`init.sh`)
To automate all steps above on an Ubuntu Server VM in Vagrant, add `init.sh` to your `Vagrantfile` (it automatically reads parameters from `.env` or `.env.example`):
```ruby
config.vm.provision "shell", path: "init.sh"
```