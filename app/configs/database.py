from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.types_users.type_user_model import TypeUserModel
    from app.models.category_products.category_model import CategoryModel
    from app.models.variations_products.variation_model import VariationModel
    from app.models.sellers.seller_model import SellerModel
    from app.models.group_products.group_model import GroupModel
    from app.models.stores.store_model import StoreModel

    from app.models.product.products_model import ProductModel

    from app.models.orders_sellers.orders_seller import OrdersModel
    from app.models.client.client_model import ClientModel
    from app.models.orders_has_products.orders_has_products import (
        OrdersHasProductsModel,
    )
    from app.models.types_sales.type_sale import TypeSaleModel
