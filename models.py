from pydantic import BaseModel
import sqlite3

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



class DataBasesetup:
    def __init__(self) -> None:
        DATABASE_URL = "sqlite:///./test.db"

        engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = self.SessionLocal()
        self.Base = declarative_base()
        self.Base.metadata.create_all(bind=engine)


DB =DataBasesetup()
Base = DB.Base


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=True, index=True)
    age = Column(Integer, nullable=True)


class UsersResponse(BaseModel):
    id: int
    name: str
    age: int
