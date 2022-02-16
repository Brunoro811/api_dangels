from dataclasses import asdict, dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship

from app.models.stores.store_model import StoreModel


@dataclass
class OrdersModel(db.Model):
    id_order: int
    date_creation: datetime
    id_store: int
    id_seller: int
    id_client: int

    __tablename__ = "orders"

    id_order = Column(sql.Integer, autoincrement=True, primary_key=True)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())

    id_seller = Column(sql.Integer, ForeignKey("sellers.id_seller"), nullable=False)
    id_client = Column(sql.Integer, ForeignKey("clients.id_client"))
    id_store = Column(sql.Integer, ForeignKey("stores.id_store"), nullable=False)
    orders_has_products_seller = relationship(
        "OrdersHasProductsModel", backref="orders", uselist=True
    )

    def __asdict__(self):
        return asdict(self)
