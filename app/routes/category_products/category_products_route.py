from flask import Blueprint

from app.controllers.category_products import category_products_controllers

bp = Blueprint("category", __name__, url_prefix="/products/category")
bp.get("")(category_products_controllers.get_all_category)
bp.post("")(category_products_controllers.create_category)
bp.patch("<int:id_category>")(category_products_controllers.update_category)
bp.delete("<int:id_category>")(category_products_controllers.deleteategory)
