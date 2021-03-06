from dataclasses import asdict, dataclass
from datetime import datetime, date

from app.configs.database import db

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship, validates


@dataclass
class ClientModel(db.Model):
    id_client: int
    first_name: str
    last_name: str
    street: str
    number: int
    zip_code: str
    country: str
    city: str
    phone: str
    email: str
    birthdate: DateTime
    cpf: str

    date_creation_user: DateTime
    name_complete: str

    __tablename__ = "clients"

    id_client = Column(sql.Integer, autoincrement=True, primary_key=True)
    first_name = Column(sql.String(20), nullable=False)
    last_name = Column(sql.String(50), nullable=False)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())
    street = Column(sql.String(100), nullable=False)
    number = Column(sql.Integer, nullable=False)
    zip_code = Column(sql.String(9), nullable=False)
    city = Column(sql.String(50), nullable=False)
    country = Column(sql.String(2), nullable=False)
    phone = Column(sql.String(14), nullable=False)
    email = Column(sql.String(100), unique=True, nullable=False)
    birthdate = Column(sql.DateTime, nullable=False)
    cpf = Column(sql.String(14), unique=True, nullable=False)
    name_complete = Column(sql.String(70), nullable=False)

    orders = relationship("OrdersModel", backref="client", uselist=True)

    def __asdict__(self):
        return asdict(self)

    @validates("first_name", "last_name")
    def title(self, key: str, value: str) -> str:
        return value.title()

    @validates("street")
    def capitalize(self, key: str, value: str) -> str:
        return value.capitalize()

    @validates("country")
    def upper_case(self, key: str, value: str) -> str:
        return value.upper()

    @validates("birthdate")
    def convert_datetime(self, key: str, value: str) -> str:
        value = value.replace("-", "/")
        value = datetime.strptime(value, "%d/%m/%Y")
        return value

    @property
    def date_creation_user(self):
        return self.date_creation_user

    @date_creation_user.getter
    def date_creation_user(self, value: str = None):

        partern = "%d/%m/%Y"
        if isinstance(
            self.date_creation,
            date,
        ):
            value = datetime.strftime(self.date_creation, partern)
        else:
            value = self.date_creation
        return value
