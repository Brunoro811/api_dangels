from flask import Blueprint

from app.controllers.sales_controllers import orders_controllers

bp = Blueprint("orders", __name__, url_prefix="/orders")

bp.post("")(orders_controllers.create_sale)
bp.get("<int:id>")(orders_controllers.get_one_sale_for_id_order)
bp.get("/seller/<int:id>/")(orders_controllers.get_all_sale_for_id_seller)
bp.delete("<int:id>")(orders_controllers.delete_sale)
