from flask import current_app, jsonify
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.decorators import verify_payload

from app.models.client.client_model import ClientModel


@verify_payload(
    fields_and_types={
        "first_name": str,
        "last_name": str,
        "street": str,
        "number": int,
        "zip_code": str,
        "country": str,
        "city": str,
        "phone": str,
        "email": str,
        "birthdate": str,
        "cpf": str,
    }
)
def create_client(data: dict):
    try:
        session: Session = current_app.db.session
        new_cliente = ClientModel(**data)

        session.add(new_cliente)
        session.commit()

        return jsonify(new_cliente), HTTPStatus.CREATED
    except IntegrityError:
        return {"error": "Cpf or email exists."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
