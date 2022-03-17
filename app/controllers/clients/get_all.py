from flask import jsonify
from http import HTTPStatus


from app.models.client.client_model import ClientModel


def get_clients():
    clients = ClientModel.query.all()

    return jsonify(clients), HTTPStatus.OK
