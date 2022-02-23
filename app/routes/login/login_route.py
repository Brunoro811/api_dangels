from flask import Blueprint

from app.controllers.login import login_controllers

bp = Blueprint("login", __name__, url_prefix="users/login")

bp.post("")(login_controllers.create_login)
