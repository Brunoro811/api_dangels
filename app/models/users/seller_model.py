from dataclasses import dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship

from app.models.users.store_model import StoreModel


@dataclass
class SellerModel(db.Model):
    id_seller: int
    first_name: str
    last_name: str
    id_store: int
    date_creation: datetime

    __tablename__ = "sellers"
    id_seller = Column(sql.Integer, autoincrement=True, primary_key=True)
    first_name = Column(sql.String(30), nullable=False)
    last_name = Column(sql.String(50), nullable=False)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())
    date_resignation = Column(sql.DateTime)
    id_store = Column(sql.Integer, ForeignKey("stores.id_store"))
    stores = relationship(
        "StoreModel", foreign_keys=[id_store], back_populates="sellers"
    )

    def __asdict__(self):
        return {
            "id_seller": self.id_seller,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "id_store": self.id_store,
            "date_creation": self.date_creation,
        }


StoreModel.sellers = relationship(
    "SellerModel", order_by=SellerModel.id_store, back_populates="stores"
)