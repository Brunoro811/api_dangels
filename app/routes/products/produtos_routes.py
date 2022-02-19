from flask import Blueprint

from app.controllers.products import products_controllers

bp = Blueprint("products", __name__, url_prefix="/products")

bp.get("")(products_controllers.get_product)
bp.get("<int:id>")(products_controllers.get_one_product)
bp.post("")(products_controllers.create_product)
bp.patch("<int:id>")(products_controllers.update_product)
bp.delete("<int:id>")(products_controllers.delete_product)

bp.post("/group")(products_controllers.create_group)
bp.get("/group")(products_controllers.get_groups)
