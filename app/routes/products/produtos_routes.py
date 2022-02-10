from flask import Blueprint

from app.controllers.products import products_controllers

bp = Blueprint("products", __name__, url_prefix="/products")

bp.get("")(products_controllers.get_product)
bp.post("")(products_controllers.create_product)
bp.patch("")(products_controllers.update_product)
bp.delete("")(products_controllers.delete_product)
