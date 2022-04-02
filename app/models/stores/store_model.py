from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import validates, relationship


@dataclass
class StoreModel(db.Model):

    id_store: int
    name_store: str
    street: str
    number: int
    zip_code: str
    other_information: str

    __tablename__ = "stores"
    id_store = Column(sql.Integer, autoincrement=True, primary_key=True)
    name_store = Column(sql.String(50), nullable=False, unique=True)
    street = Column(sql.String(150), nullable=False)
    number = Column(sql.Integer, nullable=False)
    zip_code = Column(sql.String(9), nullable=False)
    other_information = Column(sql.String(200), nullable=False)

    orders = relationship("OrdersModel", backref="store", uselist=True)

    def asdict(self):
        return asdict(self)

    @validates("name_store")
    def title_text(self, key: str, value: str) -> str:
        return value.title()

    @validates("street", "other_information")
    def capitalize_text(self, key: str, value: str):
        return value.capitalize()
