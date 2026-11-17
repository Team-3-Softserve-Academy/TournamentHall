import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URL")
if not DATABASE_URI:
    raise ValueError("Error: ensre the 'DATABASE_URL' is present at your '.env' file.")

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def get_session():
    return Session()