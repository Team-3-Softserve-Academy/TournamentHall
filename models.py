from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from database_access import Base, engine

class Lord(Base):
    __tablename__ = "lords"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    image_url = Column(String)
    house = Column(String(100))

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="check_lord_name_not_empty"),
        CheckConstraint("length(trim(login)) > 0", name="check_lord_login_not_empty"),
        CheckConstraint("length(trim(password_hash)) > 0", name="check_lord_password_not_empty"),
    )

class Knight(Base):
    __tablename__ = "knights"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    image_url = Column(String)
    strength = Column(Integer)
    speed = Column(Integer)
    protection = Column(Integer)
    house = Column(String(100))
    key = Column(String(255), unique=True)
    key_last_used = Column(DateTime)

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="check_knight_name_not_empty"),
        CheckConstraint("length(trim(login)) > 0", name="check_knight_login_not_empty"),
        CheckConstraint("length(trim(password_hash)) > 0", name="check_knight_password_not_empty"),
        CheckConstraint("strength BETWEEN 1 AND 20", name="check_knight_strength_range"),
        CheckConstraint("speed BETWEEN 1 AND 20", name="check_knight_speed_range"),
        CheckConstraint("protection BETWEEN 1 AND 20", name="check_knight_protection_range"),
    )

class CommonFolk(Base):
    __tablename__ = "commonfolks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="check_commonfolk_name_not_empty"),
        CheckConstraint("length(trim(login)) > 0", name="check_commonfolk_login_not_empty"),
        CheckConstraint("length(trim(password_hash)) > 0", name="check_commonfolk_password_not_empty"),
    )

Base.metadata.create_all(bind=engine)

