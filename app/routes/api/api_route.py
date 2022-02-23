from flask import Blueprint

from app.routes.products.produtos_routes import bp as bp_products
from app.routes.category_products.category_products_route import (
    bp as bp_category_products,
)
from app.routes.users.users_route import bp as bp_users
from app.routes.sales.orders_route import bp as bp_sale
from app.routes.stores.stores_route import bp as bp_stores
from app.routes.clients.clients_route import bp as bp_clients
from app.routes.distribute.distribute_route import bp as bp_distribute
from app.routes.login.login_route import bp as bp_login

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(bp_products)
bp.register_blueprint(bp_category_products)
bp.register_blueprint(bp_users)
bp.register_blueprint(bp_sale)
bp.register_blueprint(bp_stores)
bp.register_blueprint(bp_clients)
bp.register_blueprint(bp_distribute)
bp.register_blueprint(bp_login)
