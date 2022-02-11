from unicodedata import category
from app.configs.database import db
from dataclasses import dataclass

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, ForeignKey


@dataclass
class CategoryModel(db.Model):
    id_category: int
    name: str

    __tablename__ = "categorys"
    id_category = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(50), unique=True, nullable=False)

    @staticmethod
    def serializer(values: list[tuple]) -> dict:
        serialzier_values = [
            {"id": category.id_category, "name": category.name} for category in values
        ]
        return serialzier_values
