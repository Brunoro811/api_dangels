from dataclasses import asdict, dataclass
from datetime import date, datetime
from email.policy import default
from app.configs.database import db

from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship


@dataclass
class OrdersModel(db.Model):
    id_order: int
    date_creation_order: Date
    id_store: int
    id_seller: int
    id_client: int
    sale_finish: bool

    """ relationship """
    orders_has_products: list
    """ relationship """

    __tablename__ = "orders"

    id_order = Column(sql.Integer, autoincrement=True, primary_key=True)
    date_creation = Column(sql.Date, default=date.today())
    sale_finish = Column(sql.Boolean, nullable=False)

    id_seller = Column(sql.Integer, ForeignKey("sellers.id_seller"), nullable=False)
    id_client = Column(sql.Integer, ForeignKey("clients.id_client"))
    id_store = Column(sql.Integer, ForeignKey("stores.id_store"), nullable=False)
    orders_has_products = relationship(
        "OrdersHasProductsModel", backref="orders", uselist=True
    )

    def __asdict__(self):
        return asdict(self)

    @property
    def date_creation_order(self):
        return self.date_creation_order

    @date_creation_order.getter
    def date_creation_order(self, value: str = None):
        partern = "%d/%m/%Y"
        value = self.date_creation

        if isinstance(
            self.date_creation,
            date,
        ):
            value = datetime.strftime(self.date_creation, partern)
        return value
