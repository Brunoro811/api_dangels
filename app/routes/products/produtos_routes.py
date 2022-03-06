from flask import Blueprint

from app.controllers.products import products_controllers
from app.controllers.products import update_product

bp = Blueprint("products", __name__, url_prefix="/products")

bp.get("")(products_controllers.get_product)
bp.get("/<int:id>")(products_controllers.get_one_product)
bp.get("/images/<name>")(products_controllers.get_image_product)
bp.get("/completed")(products_controllers.get_all_product_completed)
bp.get("/group")(products_controllers.get_groups)

bp.post("")(products_controllers.create_product)
bp.post("/images/<int:id>")(products_controllers.create_images_product)

bp.patch("<int:id>")(update_product)

bp.delete("<int:id>")(products_controllers.delete_product)

bp.post("/group")(products_controllers.create_group)
