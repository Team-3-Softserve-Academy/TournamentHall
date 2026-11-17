from sqlalchemy import Column, Integer, String
from DatabaseAccess import Base, engine

class Lord(Base):
    __tablename__ = "lords"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    photo_url = Column(String)

class Knight(Base):
    __tablename__ = "knights"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    photo_url = Column(String)
    strength = Column(Integer)
    speed = Column(Integer)
    protection = Column(Integer)
    home = Column(String)

class CommonFolk(Base):
    __tablename__ = "commonfolks"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
