from flask import jsonify
from http import HTTPStatus as httpstatus

from app.models.category_products.category_model import CategoryModel


def get_all_category():
    try:
        categorys = CategoryModel.query.all()
        return jsonify(categorys), httpstatus.OK
    except Exception as e:
        raise e
