from flask import Blueprint

from app.controllers.stores import (
    create_stores,
    update_store,
    get_stores,
    get_one_store,
    delete_store,
)

bp = Blueprint("stores", __name__, url_prefix="/stores")
bp.get("")(get_stores)
bp.get("<int:id>")(get_one_store)
bp.post("")(create_stores)
bp.delete("<int:id>")(delete_store)
bp.patch("<int:id>")(update_store)
