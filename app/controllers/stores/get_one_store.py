from flask import jsonify
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound

from app.models.stores.store_model import StoreModel


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
