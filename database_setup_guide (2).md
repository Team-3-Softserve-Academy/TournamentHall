# Database Configuration & Initialization

This document explains the requirements, connection parameters, and execution process for initializing the database schema using `database.py` and `database_access.py`. It also covers essential database-level security configurations.

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

`database_access.py` reads the connection string from the `DATABASE_URL` environment variable (loaded from a `.env` file in the project root).

### URI Format
```
dialect+driver://username:password@host:port/database_name
```

### Parameter Breakdown

| Parameter | Purpose | Example Value |
| :--- | :--- | :--- |
| **`dialect`** | Defines the database type for SQL syntax generation. | `postgresql` |
| **`driver`** | *(Optional)* The Python DB-API library. | `psycopg2` |
| **`username`** | The PostgreSQL role used to authenticate. | `postgresql` |
| **`password`** | The password for the specified PostgreSQL role. | `postgresql` |
| **`host`** | The IP address/hostname of the PostgreSQL server. | `localhost` *(or DB node IP: `192.168.50.14`)* |
| **`port`** | The TCP port the PostgreSQL server listens on. | `5432` |
| **`database_name`** | The target database schema. | `tournament_db` |

## 4. Schema Initialization (`database.py`)

The `database.py` file contains the table models and a standalone execution block (`if __name__ == "__main__":`).

### How It Works
1. Imports `engine` and `Base` from `database_access.py`.
2. Registers table structures in `Base.metadata`.
3. Executes `Base.metadata.create_all(bind=engine)`, issuing `CREATE TABLE IF NOT EXISTS`.

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

**Step 3: Configure the Internal Firewall (`pg_hba.conf`)**
Dynamically locate the `pg_hba.conf` file and append a strict rule. This rule ensures that only the App Node (`192.168.50.10`) can connect to `tournament_db` using the `postgresql` user, and it enforces `scram-sha-256` password encryption.
```bash
# Find the config file path dynamically
PG_HBA=$(sudo -u postgres psql -t -P format=unaligned -c 'show hba_file')

# Add the strict access rule
echo "host tournament_db postgresql 192.168.50.10/32 scram-sha-256" | sudo tee -a $PG_HBA
```

**Step 4: Apply Changes**
Restart the PostgreSQL service to load the new network bindings and HBA rules.
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

# 3. Apply Security Hardening (Limits & Network rules)
sudo -u postgres psql -c "ALTER ROLE postgresql WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, 192.168.50.14';"
PG_HBA=$(sudo -u postgres psql -t -P format=unaligned -c 'show hba_file')
echo "host tournament_db postgresql 192.168.50.10/32 scram-sha-256" | sudo tee -a $PG_HBA
sudo systemctl restart postgresql

# 4. Setup Python Environment
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv

# 5. Configure Credentials
echo "DATABASE_URL=postgresql+psycopg2://postgresql:postgresql@192.168.50.14:5432/tournament_db" > .env

# 6. Initialize Schema
python3 database.py
```