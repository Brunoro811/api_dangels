from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import validates


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
    name_store = Column(sql.String(50), nullable=False)
    street = Column(sql.String(150), nullable=False)
    number = Column(sql.Integer, nullable=False)
    zip_code = Column(sql.String(9), nullable=False)
    other_information = Column(sql.String(200), nullable=False)

    @validates("name_store")
    def title(self, key: str, value: str):
        return value.title()

    @validates("street", "other_information")
    def title(self, key: str, value: str):
        return value.capitalize()

    def normalize(self):
        return asdict(self)
