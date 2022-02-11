from dataclasses import dataclass
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column,ForeignKey
from sqlalchemy.orm import relationship

from app.models.product.products_model import ProductModel


@dataclass
class SizeModel(db.Model):
    id_size : int
    name : str
    quantity : int
    id_product: int

    __tablename__ = "sizes_products"
    id_size = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(20), nullable=False)
    quantity = Column(sql.Integer, nullable=False)
    id_product = Column(sql.Integer, ForeignKey('products.id_product'))
    products = relationship(
        "ProductModel", foreign_keys=[id_product], back_populates="sizes_products"
    )
ProductModel.sizes_products = relationship(
    "SizeModel", order_by=SizeModel.id_product, back_populates="products"
)