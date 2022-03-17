from flask import current_app, jsonify
from http import HTTPStatus

from sqlalchemy.orm import Session

from app.models.stores.store_model import StoreModel

from app.decorators import verify_payload

from sqlalchemy.exc import IntegrityError


@verify_payload(
    fields_and_types={
        "name_store": str,
        "street": str,
        "number": int,
        "zip_code": str,
        "other_information": str,
    },
    optional=["other_information"],
)
def create_stores(data: dict):
    try:
        session: Session = current_app.db.session

        new_store = StoreModel(**data)

        session.add(new_store)
        session.commit()

        return jsonify(new_store), HTTPStatus.CREATED
    except IntegrityError as e:
        return {"error": f"{e.args[0]}"}, HTTPStatus.UNPROCESSABLE_ENTITY
