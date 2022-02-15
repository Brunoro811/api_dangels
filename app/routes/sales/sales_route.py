from flask import Blueprint

from app.controllers.sales_controllers import sales_controllers

bp = Blueprint("sales", __name__, url_prefix="/sales")

bp.post("")(sales_controllers.create_sale)

"""bp.get("")(sales_controllers.get_users)
bp.get("<int:id>")(sales_controllers.get_one_users)
bp.delete("<int:id>")(sales_controllers.delete_users)
bp.patch("<int:id>")(sales_controllers.update_users)"""
