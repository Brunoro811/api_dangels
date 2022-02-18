from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, ForeignKey


@dataclass
class VariationModel(db.Model):
    id_variation: int
    color: str
    size: str
    image: str
    id_product: int
    quantity: int

    __tablename__ = "variations"
    id_variation = Column(sql.Integer, autoincrement=True, primary_key=True)
    color = Column(sql.String(50), nullable=False)
    size = Column(sql.String(50), nullable=False)
    image = Column(sql.String(150))
    quantity = Column(sql.Integer, nullable=False)
    id_product = Column(sql.Integer, ForeignKey("products.id_product"), nullable=False)

    def asdict(self):
        return asdict(self)
