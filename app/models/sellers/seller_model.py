from dataclasses import asdict, dataclass
from datetime import datetime, date
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship, validates

from app.models.stores.store_model import StoreModel


@dataclass
class SellerModel(db.Model):
    id_seller: int
    first_name: str
    last_name: str
    id_store: int
    date_creation_seller: datetime

    """ Relationship """
    store: str
    """ Relationship """

    __tablename__ = "sellers"
    id_seller = Column(sql.Integer, autoincrement=True, primary_key=True)
    first_name = Column(sql.String(30), nullable=False)
    last_name = Column(sql.String(50), nullable=False)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())
    date_resignation = Column(sql.DateTime)
    id_store = Column(sql.Integer, ForeignKey("stores.id_store"))
    store = relationship(
        "StoreModel", foreign_keys=[id_store], back_populates="sellers"
    )
    orders = relationship("OrdersModel", backref="sellers", uselist=True)

    def asdict(self):
        return asdict(self)

    @validates("first_name", "last_name")
    def title(self, key: str, value: str):
        return value.title()

    @property
    def date_creation_seller(self):
        return self.date_creation_seller

    @date_creation_seller.getter
    def date_creation_seller(self, value: str = None):
        partern = "%d/%m/%Y"
        value = self.date_creation
        if isinstance(
            self.date_creation,
            date,
        ):
            value = datetime.strftime(self.date_creation, partern)
        return value


StoreModel.sellers = relationship(
    "SellerModel", order_by=SellerModel.id_store, back_populates="store"
)
