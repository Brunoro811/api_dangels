from http import HTTPStatus
from flask import jsonify

from app.models.product.products_model import ProductModel


def get_all_products_for_store(id: int):
    try:
        products = ProductModel.query.filter_by(id_store=id).all()

        return jsonify(products), HTTPStatus.OK
    except Exception as e:
        raise e
