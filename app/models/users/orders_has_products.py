from dataclasses import asdict, dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship

from app.models.stores.store_model import StoreModel


@dataclass
class OrdersHasProductsModel(db.Model):
    id_order_has_products: int
    sale_value: float
    quantity: int
    color: str
    size: str
    id_product: int
    id_order: int

    __tablename__ = "orders_has_products"

    id_order_has_products = Column(sql.Integer, autoincrement=True, primary_key=True)
    sale_value = Column(sql.Float(2), nullable=False)
    quantity = Column(sql.Integer, nullable=False)
    color = Column(sql.String(50), nullable=False)
    size = Column(sql.String(10), nullable=False)

    id_product = Column(sql.Integer, ForeignKey("products.id_product"), nullable=False)
    id_order = Column(sql.Integer, ForeignKey("orders.id_order"), nullable=False)

    def __asdict__(self):
        return asdict(self)
