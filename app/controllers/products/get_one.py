from flask import jsonify
from http import HTTPStatus


from sqlalchemy.orm.exc import NoResultFound


from app.controllers.products.products_helpers import help_normalize_variations
from app.models.product.products_model import ProductModel


def get_one_product(id: int):
    try:
        product: ProductModel = ProductModel.query.get(id)
        if not product:
            raise NoResultFound

        obj_product_completed = {}
        obj_product_completed = {
            **product.asdict(),
            **help_normalize_variations(product.variations)[0],
        }

        return jsonify(obj_product_completed), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
