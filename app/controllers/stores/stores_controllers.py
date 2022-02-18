from flask import current_app, jsonify, request
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.stores.store_model import StoreModel
from app.controllers.decorators import verify_keys, verify_types


@verify_keys(["name_store", "number", "other_information", "street", "zip_code"])
@verify_types(
    {
        "name_store": str,
        "street": str,
        "number": int,
        "zip_code": str,
        "other_information": str,
    }
)
def create_stores():
    session: Session = current_app.db.session

    data = request.get_json()
    new_store = StoreModel(**data)
    new_new_store = new_store.normalize()
    new_new_store.pop("id_store")

    session.add(new_store)
    session.commit()

    return jsonify(new_store), HTTPStatus.CREATED


def get_stores():
    try:
        stores_all = StoreModel.query.all()

        return jsonify(stores_all), HTTPStatus.OK
    except Exception as e:
        raise e


def get_one_store(id: int):
    try:
        store = StoreModel.query.get(id)
        if not (store):
            raise NoResultFound

        return jsonify(store), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found store."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


def delete_store(id: int):
    session: Session = current_app.db.session
    try:
        store = StoreModel.query.get(id)
        if not (store):
            raise NoResultFound
        session.delete(store)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found store."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


@verify_keys(
    ["name_store", "number", "other_information", "street", "zip_code"],
    optional_keys=True,
)
@verify_types(
    {
        "name_store": str,
        "street": str,
        "number": int,
        "zip_code": str,
        "other_information": str,
    },
    optional_keys=True,
)
def update_store(id: int):
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
