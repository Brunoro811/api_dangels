from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql

from app.models.product.products_model import ProductModel


@dataclass
class OrdersHasProductsModel(db.Model):
    sale_value: float
    quantity: int
    color: str
    size: str
    id_product: int
    id_order: int
    product: dict

    __tablename__ = "orders_has_products"

    id_order_has_products = Column(sql.Integer, autoincrement=True, primary_key=True)
    sale_value = Column(sql.Float(2), nullable=False)
    quantity = Column(sql.Integer, nullable=False)
    color = Column(sql.String(50), nullable=False)
    size = Column(sql.String(10), nullable=False)

    id_product = Column(sql.Integer, ForeignKey("products.id_product"), nullable=False)
    id_order = Column(sql.Integer, ForeignKey("orders.id_order"), nullable=False)

    @property
    def product(self):
        return self.product

    @product.getter
    def product(self, value: ProductModel) -> ProductModel:
        value = ProductModel.query.get(self.id_product)
        return value

    def __asdict__(self):
        return asdict(self)
