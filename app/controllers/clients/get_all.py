from flask import current_app, jsonify, request
from http import HTTPStatus
from sqlalchemy.orm import Session, Query


from app.models.client.client_model import ClientModel


def get_clients():

    print(request.args.to_dict())
    print("")
    print(request.args.get("search"))
    clients: list[ClientModel] = []
    search: str = request.args.get("search")
    if search:
        session: Session = current_app.db.session
        clients = (
            session.query(ClientModel)
            .filter(ClientModel.first_name == search.title())
            .all()
        )
    else:
        clients = ClientModel.query.all()

    return jsonify(clients), HTTPStatus.OK
