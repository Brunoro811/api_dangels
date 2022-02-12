from dataclasses import dataclass
from app.configs.database import db

from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as sql

@dataclass
class StoreModel(db.Model):
    id_store : int
    name_store : str
    adress : str

    __tablename__ = "stores"
    id_store = Column(sql.Integer,autoincrement=True,primary_key=True)
    name_store = Column(sql.String(50),nullable=False)
    adress = Column(sql.String(50),nullable=False)