from flask import current_app, jsonify
from http import HTTPStatus

from sqlalchemy.orm import Session

from app.models.stores.store_model import StoreModel

from app.decorators import verify_payload


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
    session: Session = current_app.db.session

    new_store = StoreModel(**data)

    session.add(new_store)
    session.commit()

    return jsonify(new_store), HTTPStatus.CREATED
