from dataclasses import dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship

from app.models.users.users_model import UsersModel

@dataclass
class DisabledUsers(db.Model):
    
    id_disabled: int
    id_user: int
    name: str
    date_disabled: int

    __tablename__ = "disabled"
    id_disabled = Column(sql.Integer,autoincrement=True,primary_key=True)
    name = Column(sql.String(20),nullable=False)
    date_disabled = Column(sql.DateTime, default=datetime.utcnow())
    id_user = Column(sql.Integer,ForeignKey("users.id_user"))
    users = relationship("UsersModel", foreign_keys=[id_user] ,back_populates="disabled")

UsersModel.disabled = relationship(
    "DisabledUsers", order_by=DisabledUsers.id_user, back_populates="users"
)
