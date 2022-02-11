from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.product.images_model import ImagesModel
    from app.models.product.products_model import ProductModel
    from app.models.product.size_model import SizeModel
    from app.models.category_products.category_model import CategoryModel
