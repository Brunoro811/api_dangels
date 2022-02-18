from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship

from app.models.users.seller_model import SellerModel
from app.models.users.type_user_model import TypeUserModel


@dataclass
class UsersModel(db.Model):

    id_user: int
    user_name: str
    password: str
    id_type_user: int
    id_seller: int
    email: str

    __tablename__ = "users"
    id_user = Column(sql.Integer, autoincrement=True, primary_key=True)
    user_name = Column(sql.String(20), unique=True, nullable=False)
    password = Column(sql.String(30), nullable=False)
    id_desabled = Column(sql.Integer)
    id_type_user = Column(sql.Integer, ForeignKey("types_users.id_type_user"))
    id_seller = Column(sql.Integer, ForeignKey("sellers.id_seller"))
    email = Column(sql.String(100), unique=True, nullable=False)

    types_users = relationship(
        "TypeUserModel", foreign_keys=[id_type_user], back_populates="users"
    )
    sellers = relationship(
        "SellerModel", foreign_keys=[id_seller], back_populates="users"
    )

    def asdict(self):
        return asdict(self)

    def __asdict__(self):
        return {
            "id_user": self.id_user,
            "user_name": self.user_name,
            "password": self.password,
            "id_type_user": self.id_type_user,
            "id_seller": self.id_seller,
        }


TypeUserModel.users = relationship(
    "UsersModel", order_by=UsersModel.id_type_user, back_populates="types_users"
)

SellerModel.users = relationship(
    "UsersModel", order_by=UsersModel.id_seller, back_populates="sellers"
)
