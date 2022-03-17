from flask import jsonify
from http import HTTPStatus


from app.models.stores.store_model import StoreModel


def get_stores():
    try:
        stores_all = StoreModel.query.all()

        return jsonify(stores_all), HTTPStatus.OK
    except Exception as e:
        raise e
