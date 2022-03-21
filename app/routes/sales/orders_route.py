from flask import Blueprint

from app.controllers.sales import orders_controllers

from app.controllers.sales import (
    create_sale,
    get_one_sale_for_id_order,
    get_all_sale_for_id_seller,
    delete_sale,
)

bp = Blueprint("orders", __name__, url_prefix="/orders")

bp.get("/seller/<int:id>/")(get_all_sale_for_id_seller)
bp.get("<int:id>")(get_one_sale_for_id_order)
bp.post("")(create_sale)


bp.delete("<int:id>")(delete_sale)
