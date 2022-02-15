from dataclasses import dataclass
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column


@dataclass
class GroupModel(db.Model):
    id_group: int
    id_product_one: int
    id_product_two: int

    __tablename__ = "group_products"
    id_group = Column(sql.Integer, primary_key=True, autoincrement=True)
    id_product_one = Column(sql.Integer, nullable=False, unique=True)
    id_product_two = Column(sql.Integer, nullable=False, unique=True)
