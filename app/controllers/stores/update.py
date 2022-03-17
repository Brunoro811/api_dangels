from flask import current_app, request
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.stores.store_model import StoreModel
from app.decorators import verify_payload, validator


@validator(zip_code="zip_code")
@verify_payload(
    fields_and_types={
        "name_store": str,
        "street": str,
        "number": int,
        "zip_code": str,
        "other_information": str,
    },
    optional=[
        "name_store",
        "street",
        "number",
        "zip_code",
        "other_information",
    ],
)
def update_store(data: dict, id: int):
    session: Session = current_app.db.session
    try:
        storie = StoreModel.query.get(id)
        if not (storie):
            raise NoResultFound

        data: dict = request.get_json()
        for key, value in data.items():
            if key == "name_store":
                value = value.title()
            else:
                value = value.capitalize()

            setattr(storie, key, value)
            session.add(storie)
            session.commit()
        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found store."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
