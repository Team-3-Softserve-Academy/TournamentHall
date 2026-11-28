from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, CheckConstraint, text
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

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Base=declarative_base()
Session=sessionmaker(engine)

class User(Base):
    __tablename__="users"
    __table_args__ = (
        CheckConstraint("role IN ('Lord', 'Knight', 'CommonFolk')", name="ck_users_role"),
    )

    id=Column(Integer, primary_key=True)
    login=Column(String(100), unique=True, nullable=False)
    password_hash=Column(String(100), nullable=False)
    role=Column(String(20), nullable=False)

class Lord(Base):
    __tablename__="lords"

    id=Column(Integer, primary_key=True)
    full_name=Column(String(100), nullable=False)
    photo_url=Column(String(250))
    house=Column(String(100), nullable=False)

    user_id=Column(ForeignKey("users.id"), unique=True, nullable=False)

class Knight(Base):
    __tablename__="knights"
    __table_args__ = (
        CheckConstraint("strength BETWEEN 1 AND 20", name="ck_knights_strength"),
        CheckConstraint("dexterity BETWEEN 1 AND 20", name="ck_knights_dexterity"),
        CheckConstraint("protection BETWEEN 1 AND 20", name="ck_knights_protection"),
    )

    id=Column(Integer, primary_key=True)
    full_name=Column(String(100), nullable=False)
    photo_url=Column(String(250))
    house=Column(String(100))
    motto=Column(String(200))
    strength=Column(Integer, nullable=False)
    dexterity=Column(Integer, nullable=False)
    protection=Column(Integer, nullable=False)
    key_hash=Column(String(100))
    key_last_updated=Column(DateTime)
    is_white_knight=Column(Boolean, nullable=False, default=False, server_default=text("false"))

    user_id=Column(ForeignKey("users.id"), unique=True, nullable=False)
  
class CommonFolk(Base):
    __tablename__="commonfolks"

    id=Column(Integer, primary_key=True)
    full_name=Column(String(100), nullable=False)

    user_id=Column(ForeignKey("users.id"), unique=True, nullable=False)
