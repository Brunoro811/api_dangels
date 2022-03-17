from flask import current_app, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
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
    },
    optional=[
        "first_name",
        "last_name",
        "street",
        "number",
        "zip_code",
        "country",
        "city",
        "phone",
        "email",
        "birthdate",
        "cpf",
    ],
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
