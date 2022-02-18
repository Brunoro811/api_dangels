from dataclasses import asdict, dataclass
from app.configs.database import db

from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as sql


@dataclass
class TypeUserModel(db.Model):

    id_type_user: int
    name_type_user: str
    permission: int

    __tablename__ = "types_users"
    id_type_user = Column(sql.Integer, autoincrement=True, primary_key=True)
    name_type_user = Column(sql.String(20), nullable=False)
    permission = Column(sql.Integer, nullable=False)

    def asdict(self):
        return asdict(self)

    def __asdict__(self):
        return {
            "id_type_user": self.id_type_user,
            "name_type_user": self.name_type_user,
            "permission": self.permission,
        }
