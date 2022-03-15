from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import validates


@dataclass
class VariationModel(db.Model):
    id_variation: int
    color: str
    size: str
    id_product: int
    quantity: int

    __tablename__ = "variations"
    id_variation = Column(sql.Integer, autoincrement=True, primary_key=True)
    color = Column(sql.String(50), nullable=False)
    size = Column(sql.String(50), nullable=False)
    quantity = Column(sql.Integer, nullable=False)
    id_product = Column(sql.Integer, ForeignKey("products.id_product"), nullable=False)

    def asdict(self):
        return asdict(self)

    @validates("size")
    def uppeer_case(self, key: str, value: str):
        return value.upper()

    @validates("title")
    def title(self, key: str, value: str):
        return value.title()
