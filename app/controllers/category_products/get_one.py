from flask import jsonify
from http import HTTPStatus as httpstatus

from app.models.category_products.category_model import CategoryModel

from sqlalchemy.orm.exc import NoResultFound


def get_category(id_category: int):
    try:
        category = CategoryModel.query.get(id_category)
        if not category:
            raise NoResultFound

        return jsonify(category), httpstatus.OK
    except NoResultFound:
        return {"error": "Not found category."}, httpstatus.NOT_FOUND
    except Exception as e:
        raise e
