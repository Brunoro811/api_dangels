from flask import Blueprint

from app.controllers.stores import stores_controllers

bp = Blueprint("stores", __name__, url_prefix="/stores")
bp.get("")(stores_controllers.get_stores)
bp.get("<int:id>")(stores_controllers.get_one_store)
bp.post("")(stores_controllers.create_stores)
bp.delete("<int:id>")(stores_controllers.delete_store)
bp.patch("<int:id>")(stores_controllers.update_store)
