from dataclasses import asdict, dataclass
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship

from app.models.users.seller_model import SellerModel
from app.models.users.type_user_model import TypeUserModel
from app.configs.database import db


@dataclass
class UsersModel(db.Model):

    id_user: int
    user_name: str
    id_type_user: int
    id_seller: int
    email: str

    __tablename__ = "users"
    id_user = Column(sql.Integer, autoincrement=True, primary_key=True)
    user_name = Column(sql.String(20), unique=True, nullable=False)
    password_hash = Column(sql.String(255), nullable=True)
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

    @property
    def password(self):
        raise AttributeError("password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)


TypeUserModel.users = relationship(
    "UsersModel", order_by=UsersModel.id_type_user, back_populates="types_users"
)

SellerModel.users = relationship(
    "UsersModel", order_by=UsersModel.id_seller, back_populates="sellers"
)
