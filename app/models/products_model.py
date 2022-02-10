from dataclasses import dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models.category_products.category_model import CategoryModel


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


"""
@dataclass
class ProductSetModel(db.Model):
    id_product_set = int
    product_one = int
    product_two = int

    __tablename__ = "products_set"
    id_product_set = Column(sql.Integer, autoincrement=True, primary_key=True)
    id_product_one = Column(sql.Integer)
    id_product_two = Column(sql.Integer)
"""


@dataclass
class SizeModel(db.Model):
    id_size : int
    name : str
    quantity : int

    __tablename__ = "sizes_products"
    id_size = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(20), nullable=False)
    quantity = Column(sql.Integer, nullable=False)


@dataclass
class ProductModel(db.Model):
    id_product: int
    name: str
    id_category: int
    cost: float
    date_creation: datetime
    id_images: int
    # id_product_set: int

    __tablename__ = "products"
    id_product = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(50), nullable=False)
    cost = Column(sql.Float, nullable=False)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())
    id_category = Column(
        sql.Integer, ForeignKey("categorys.id_category"), nullable=False
    )
    id_images = Column(sql.Integer, ForeignKey("images_products.id_images"))
    # id_product_set = Column(sql.Integer, ForeignKey("products_set.id_product_set"))
    categorys = relationship(
        "CategoryModel", foreign_keys=[id_category], back_populates="products"
    )
    images_products = relationship(
        "ImagesModel", foreign_keys=[id_images], back_populates="products"
    )
    # product_set = relationship(
    #    "ProductSetModel", foreign_keys=[id_product_set], back_populates="products"
    # )


CategoryModel.products = relationship(
    "ProductModel", order_by=ProductModel.id_category, back_populates="categorys"
)
ImagesModel.products = relationship(
    "ProductModel", order_by=ProductModel.id_images, back_populates="images_products"
)
# ProductSetModel.products = relationship(
#    "ProductModel", order_by=ProductModel.id_product_set, back_populates="product_set"
# )


@dataclass
class ProductHaveSizeModel(db.Model):
    id_product_have_size : int
    id_product : int
    id_size : int

    __tablename__ = "product_have_sizes"
    id_product_have_size = Column(sql.Integer, autoincrement=True, primary_key=True)
    id_product = Column(sql.Integer, ForeignKey("products.id_product"), nullable=False)
    id_size = Column(sql.Integer, ForeignKey("sizes_products.id_size"), nullable=False)
    products = relationship(
        "ProductModel", foreign_keys=[id_product], back_populates="product_have_sizes"
    )
    size_products = relationship(
        "SizeModel", foreign_keys=[id_size], back_populates="product_have_sizes"
    )


ProductModel.product_have_sizes = relationship(
    "ProductHaveSizeModel",
    order_by=ProductHaveSizeModel.id_product,
    back_populates="products",
)
SizeModel.product_have_sizes = relationship(
    "ProductHaveSizeModel",
    order_by=ProductHaveSizeModel.id_size,
    back_populates="size_products",
)
