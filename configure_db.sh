# Setup Python Environment
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv

# Initialize schema creating tables for the target database
python3 models.py