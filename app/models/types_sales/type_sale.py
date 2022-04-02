from dataclasses import asdict, dataclass
from app.configs.database import db
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column


@dataclass
class TypeSaleModel(db.Model):
    id_type_sale: int
    name: str
    commission_amount: float

    __tablename__ = "types_sales"

    id_type_sale = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(50), nullable=False)
    commission_amount = Column(sql.Float, nullable=False)

    def asdict(self):
        return asdict(self)
