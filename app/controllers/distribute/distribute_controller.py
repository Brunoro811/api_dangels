from http import HTTPStatus
from flask import current_app, jsonify, request

from app.auth import verify_token

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.controllers.exc.user_erros import BodyNoContent
from app.models.product.variation_model import VariationModel

from app.models.product.products_model import ProductModel
from app.models.stores.store_model import StoreModel


def create_distribute_product():
    session: Session = current_app.db.session
    try:
        if not (request.get_json()):
            raise BodyNoContent("JSON empty or not found")
        data = request.get_json()

        storie = StoreModel.query.get(data["id_store"])
        if not storie:
            raise NoResultFound

        product: ProductModel = ProductModel.query.get(data["id_product"])
        if not (product):
            raise NoResultFound

        new_product = {**product.asdict(), "id_product": None, "id_store": None}
        new_product.pop("link_image")
        new_product = ProductModel(**new_product)
        new_product.variations = [
            VariationModel(
                **{
                    **element.asdict(),
                    "id_variation": None,
                    "id_product": new_product.id_product,
                }
            )
            for element in product.variations
        ]
        new_product.id_store = data["id_store"]
        for color_size_update in data["products"]:
            if not color_size_update["id_product"] == data["id_product"]:
                raise NoResultFound

            for product_variations_base_data in new_product.variations:
                if (
                    product_variations_base_data.color.lower()
                    == color_size_update["color"].lower()
                    and product_variations_base_data.size == color_size_update["size"]
                ):
                    for key, value in color_size_update.items():
                        setattr(product_variations_base_data, key, value)

        session.add(new_product)
        session.commit()
        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except BodyNoContent as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


@verify_token
def get_all_products_for_store(id: int):
    try:
        products = ProductModel.query.filter_by(id_store=id).all()

        return jsonify(products), HTTPStatus.OK
    except Exception as e:
        raise e
