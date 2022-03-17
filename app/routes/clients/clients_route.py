from flask import Blueprint

from app.controllers.clients import (
    create_client,
    delete_client,
    get_clients,
    get_one_client,
    update_client,
)

bp = Blueprint("clients", __name__, url_prefix="/clients")

bp.get("")(get_clients)
bp.get("<int:id>")(get_one_client)
bp.post("")(create_client)
bp.patch("<int:id>")(update_client)
bp.delete("<int:id>")(delete_client)
