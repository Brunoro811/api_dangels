from flask import current_app, jsonify, request
from http import HTTPStatus
from sqlalchemy.orm import Session, Query


from app.models.client.client_model import ClientModel


def get_clients():

    clients: list[ClientModel] = None
    search: str = request.args.get("search")
    if search:
        session: Session = current_app.db.session
        clients = (
            session.query(ClientModel)
            .filter(ClientModel.first_name.like(f"%{search[1:len(search)]}%"))
            .all()
        )

    else:
        clients = ClientModel.query.all()

    return jsonify(clients), HTTPStatus.OK
