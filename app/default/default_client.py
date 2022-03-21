from flask import current_app
from sqlalchemy.orm import Session

from app.models.client.client_model import ClientModel

from app.default.default_values import client


def default_client():
    try:

        session: Session = current_app.db.session
        all_clients: ClientModel = ClientModel.query.all()
        if not all_clients:
            client_default: ClientModel = ClientModel(**client)
            session.add(client_default)
            session.commit()

    except Exception as e:
        raise e
