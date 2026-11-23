from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Base=declarative_base()
Session=sessionmaker(engine)
session=Session()

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True)
    login=Column(String(100), unique=True)
    password_hash=Column(String(100), nullable=False)
    role=Column(String(20))

class Lord(Base):
    __tablename__="lords"

    id=Column(Integer, primary_key=True)
    full_name=Column(String(100))
    photo_url=Column(String(250))
    home=Column(String(100))

    user_id=Column(ForeignKey("users.id"))

class Knight(Base):
    __tablename__="knights"

    id=Column(Integer, primary_key=True)
    full_name=Column(String(100))
    photo_url=Column(String(250))
    home=Column(String(100))
    motto=Column(String(200))
    strength=Column(Integer)
    protection=Column(Integer)
    speed=Column(Integer)
    key_hash=Column(String(100))
    key_last_updated=Column(DateTime)
    is_white_knight=Column(Boolean)

    user_id=Column(ForeignKey("users.id"))
  
class CommonFolk(Base):
    __tablename__="commonfolks"

    id=Column(Integer, primary_key=True)
    name=Column(String(100))

    user_id=Column(ForeignKey("users.id"))

Base.metadata.create_all(engine)