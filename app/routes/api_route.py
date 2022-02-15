from flask import Blueprint

from app.routes.products.produtos_routes import bp as bp_products
from app.routes.category_products.category_products_route import (
    bp as bp_category_products,
)
from app.routes.users.users_route import bp as bp_users
from app.routes.sales.sales_route import bp as bp_sale
from app.routes.stores.stores_route import bp as bp_stores

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(bp_products)
bp.register_blueprint(bp_category_products)
bp.register_blueprint(bp_users)
bp.register_blueprint(bp_sale)
bp.register_blueprint(bp_stores)
