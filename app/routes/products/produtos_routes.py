from flask import Blueprint

from app.controllers.products import products_controllers

bp = Blueprint("products", __name__, url_prefix="/products")

bp.get("")(products_controllers.get_product)
bp.get("<int:id_product>")(products_controllers.get_one_product)
bp.post("")(products_controllers.create_product)
bp.patch("<int:id_product>")(products_controllers.update_product)
bp.delete("<int:id_product>")(products_controllers.delete_product)
