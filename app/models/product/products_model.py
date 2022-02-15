from dataclasses import dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


@dataclass
class ProductModel(db.Model):
    id_product: int
    code_product: int
    name: str
    cost_value: float
    sale_value: float
    id_category: int

    date_creation: datetime

    __tablename__ = "products"
    id_product = Column(sql.Integer, autoincrement=True, primary_key=True)
    code_product = Column(sql.Integer, unique=True)
    name = Column(sql.String(50), nullable=False)
    cost_value = Column(sql.Float(2), nullable=False)
    sale_value = Column(sql.Float(2), nullable=False)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())
    id_category = Column(
        sql.Integer, ForeignKey("categorys.id_category"), nullable=False
    )
    variations = relationship("VariationModel", backref="product", uselist=True)

    def asdict(self):
        return {
            "id_product": self.id_product,
            "name": self.name,
            "cost_value": self.cost_value,
            "cost_value": self.cost_value,
            "date_creation": self.date_creation,
            "id_category": self.id_category,
        }
