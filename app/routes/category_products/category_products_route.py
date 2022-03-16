from flask import Blueprint

from app.controllers.category_products import (
    create_category,
    update_category,
    delete_category,
    get_all_category,
    get_category,
)

bp = Blueprint("category", __name__, url_prefix="/products/category")
bp.get("")(get_all_category)
bp.get("<int:id_category>")(get_category)

bp.post("")(create_category)
bp.patch("<int:id_category>")(update_category)
bp.delete("<int:id_category>")(delete_category)
