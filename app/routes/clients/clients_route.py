from flask import Blueprint

from app.controllers.clients_controllers import clients_controllers

bp = Blueprint("clients", __name__, url_prefix="/clients")

bp.get("")(clients_controllers.get_clients)
bp.get("<int:id>")(clients_controllers.get_one_client)
bp.post("")(clients_controllers.create_client)
bp.patch("<int:id>")(clients_controllers.update_client)
bp.delete("<int:id>")(clients_controllers.delete_client)
