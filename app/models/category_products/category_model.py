from app.configs.database import db
from dataclasses import dataclass

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column
from sqlalchemy.orm import validates


@dataclass
class CategoryModel(db.Model):
    id_category: int
    name: str

    __tablename__ = "categorys"
    id_category = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(50), unique=True, nullable=False)
    products = db.relationship("ProductModel", backref="category")

    @validates("name")
    def title(self, key, value: str):
        return value.title()
