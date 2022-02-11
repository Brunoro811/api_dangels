from flask import Blueprint

from app.routes.products.produtos_routes import bp as bp_products
from app.routes.category_products.category_products_route import (
    bp as bp_category_products,
)

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(bp_products)
bp.register_blueprint(bp_category_products)
