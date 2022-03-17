from flask import current_app, session
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.client.client_model import ClientModel


def delete_client(id: int):
    session: Session = current_app.db.session
    try:
        client = ClientModel.query.get(id)
        if not client:
            raise NoResultFound

        session.delete(client)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found client."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
