from flask import Blueprint
from app.controllers.users import users_controllers

bp = Blueprint('users', __name__, url_prefix="/users")

bp.get('')()
bp.post('')(users_controllers.create_users)
bp.delete('')()
bp.patch('')()