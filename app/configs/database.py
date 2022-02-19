from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.product.products_model import ProductModel
    from app.models.category_products.category_model import CategoryModel
    from app.models.product.variation_model import VariationModel
    from app.models.product.group_model import GroupModel

    from app.models.users.disabled_users import DisabledUsers
    from app.models.users.seller_model import SellerModel
    from app.models.stores.store_model import StoreModel
    from app.models.users.type_user_model import TypeUserModel
    from app.models.users.users_model import TypeUserModel

    from app.models.users.orders_seller import OrdersModel
    from app.models.client.client_model import ClientModel
    from app.models.users.orders_has_products import OrdersHasProductsModel

    from app.models.product_base.products_model import ProductModelBase
    from app.models.product_base.variation_model import VariationModelBase