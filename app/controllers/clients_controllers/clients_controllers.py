from flask import current_app, jsonify, request, session
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from app.controllers.decorators import verify_keys, verify_optional_keys
from app.models.client.client_model import ClientModel


@verify_keys(
    [
        "birthdate",
        "city",
        "country",
        "cpf",
        "email",
        "first_name",
        "last_name",
        "number",
        "phone",
        "street",
        "zip_code",
    ]
)
def create_client():
    try:
        session: Session = current_app.db.session
        data = request.get_json()
        new_cliente = ClientModel(**data)

        session.add(new_cliente)
        session.commit()

        return jsonify(new_cliente), HTTPStatus.CREATED
    except IntegrityError:
        return {"error": "Cpf or email exists."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


def get_clients():
    clients = ClientModel.query.all()

    return jsonify(clients), HTTPStatus.OK


def get_one_client(id: int):
    try:
        client = ClientModel.query.get(id)
        if not client:
            raise NoResultFound
        return jsonify(client), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found client."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


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


@verify_optional_keys(
    [
        "birthdate",
        "city",
        "country",
        "cpf",
        "email",
        "first_name",
        "last_name",
        "number",
        "phone",
        "street",
        "zip_code",
    ]
)
def update_client(id: int):
    session: Session = current_app.db.session
    try:
        client = ClientModel.query.get(id)
        if not client:
            raise NoResultFound
        data: dict = request.get_json()

        for key, value in data.items():
            setattr(client, key, value)

        session.add(client)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found client."}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {"error": "Cpf or email exists."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e