from dataclasses import dataclass
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column

@dataclass
class ImagesModel(db.Model):
    id_images : int
    image_one : str
    image_two : str
    image_three : str

    __tablename__ = "images_products"
    id_images = Column(sql.Integer, autoincrement=True, primary_key=True)
    image_one = Column(sql.String(100))
    image_two = Column(sql.String(100))
    image_three = Column(sql.String(100))

