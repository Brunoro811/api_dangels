from flask import Blueprint

from app.controllers.users import (
    delete_users,
    update_users,
    get_one_users,
    get_users,
    create_users,
)

bp = Blueprint("users", __name__, url_prefix="/users")

bp.get("")(get_users)
bp.get("<int:id>")(get_one_users)

bp.post("")(create_users)
bp.delete("<int:id>")(delete_users)
bp.patch("<int:id>")(update_users)
