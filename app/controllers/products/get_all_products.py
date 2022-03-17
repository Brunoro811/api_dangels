from flask import jsonify
from http import HTTPStatus

from app.models.product.products_model import ProductModel


def get_all_products_all_stores():
    product_list: ProductModel = ProductModel.query.all()
    product_list_completed = []
    for product in product_list:
        product: ProductModel
        product_completed = {}
        product_completed = {**product.asdict(), **product.store.asdict()}
        product_list_completed.append(product_completed)

    return jsonify(product_list_completed), HTTPStatus.OK
