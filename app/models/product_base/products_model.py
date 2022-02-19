from dataclasses import asdict, dataclass
from datetime import date

from flask import current_app
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import relationship


@dataclass
class ProductModelBase(db.Model):
    id_product: int
    code_product: int
    name: str
    cost_value: float
    sale_value_varejo: float
    sale_value_atacado: float
    quantity_atacado: int
    sale_value_promotion: float
    date_start: Date
    date_end: Date
    id_category: int
    date_creation: Date

    __tablename__ = "products_base"
    id_product = Column(sql.Integer, autoincrement=True, primary_key=True)
    code_product = Column(sql.Integer, unique=True)
    name = Column(sql.String(50), nullable=False)
    date_creation = Column(sql.Date, default=date.today())
    cost_value = Column(sql.Float(2), nullable=False)
    sale_value_varejo = Column(sql.Float(2), nullable=False)
    sale_value_atacado = Column(sql.Float(2), nullable=False)
    quantity_atacado = Column(sql.Integer, nullable=False)
    sale_value_promotion = Column(sql.Float(2))
    date_start = Column(sql.Date, default=date.today())
    date_end = Column(sql.Date, default=date.today())
    id_category = Column(
        sql.Integer, ForeignKey("categorys.id_category"), nullable=False
    )

    variations = relationship(
        "VariationModelBase", backref="product_base", uselist=True
    )

    def asdict(self):
        return asdict(self)

    def sale_product(self, product_variation: dict):
        for color_size_stock in self.variations:
            if (
                color_size_stock.color == product_variation["color"]
                and color_size_stock.size == product_variation["size"]
            ):
                setattr(
                    color_size_stock,
                    "quantity",
                    (color_size_stock.quantity - product_variation["quantity"]),
                )
