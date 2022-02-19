from flask import Blueprint

from app.controllers.distribute import distribute_controller

bp = Blueprint("distribute", __name__, url_prefix="products/distribute")

bp.post("")(distribute_controller.create_distribute_product)
bp.get("<int:id>")(distribute_controller.get_all_products_for_store)
