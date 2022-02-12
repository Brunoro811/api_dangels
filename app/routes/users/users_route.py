from flask import Blueprint
from app.controllers.users import users_controllers

bp = Blueprint("users", __name__, url_prefix="/users")

bp.get("")(users_controllers.get_users)
bp.get("<int:id>")(users_controllers.get_one_users)
bp.post("")(users_controllers.create_users)
bp.delete("<int:id>")(users_controllers.delete_users)
bp.patch("<int:id>")(users_controllers.update_users)
