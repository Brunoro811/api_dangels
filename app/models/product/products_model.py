from dataclasses import dataclass
from datetime import datetime
from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models.category_products.category_model import CategoryModel
from app.models.product.images_model import ImagesModel



@dataclass
class ProductModel(db.Model):
    id_product: int
    name: str
    id_category: int
    cost: float
    date_creation: datetime
    id_images: int

    __tablename__ = "products"
    id_product = Column(sql.Integer, autoincrement=True, primary_key=True)
    name = Column(sql.String(50), nullable=False)
    cost = Column(sql.Float, nullable=False)
    date_creation = Column(sql.DateTime, default=datetime.utcnow())
    id_category = Column(
        sql.Integer, ForeignKey("categorys.id_category"), nullable=False
    )
    id_images = Column(sql.Integer, ForeignKey("images_products.id_images"))
    categorys = relationship(
        "CategoryModel", foreign_keys=[id_category], back_populates="products"
    )
    images_products = relationship(
        "ImagesModel", foreign_keys=[id_images], back_populates="products"
    )
    
    def asdict (self):
        return {
                "id_product": self.id_product, 
                "name": self.name, 
                "cost": self.cost,
                "date_creation": self.date_creation, 
                "id_category": self.id_category,
                "id_images": self.id_images    
            }

CategoryModel.products = relationship(
    "ProductModel", order_by=ProductModel.id_category, back_populates="categorys"
)
ImagesModel.products = relationship(
    "ProductModel", order_by=ProductModel.id_images, back_populates="images_products"
)
