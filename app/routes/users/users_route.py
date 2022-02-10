from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix="/users")

bp.get('')()
bp.post('')()
bp.delete('')()
bp.patch('')()