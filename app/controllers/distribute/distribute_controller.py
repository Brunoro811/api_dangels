from http import HTTPStatus
from flask import current_app, jsonify, request

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.controllers.exc.user_erros import BodyNoContent
from app.models.product.variation_model import VariationModel
from app.models.product_base.products_model import ProductModelBase
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

        product: ProductModelBase = ProductModelBase.query.get(data["id_product"])
        if not (product):
            raise NoResultFound
        for color_size_update in data["products"]:
            for product_variations_base_data in product.variations:
                if (
                    product_variations_base_data.color.lower()
                    == color_size_update["color"].lower()
                    and product_variations_base_data.size == color_size_update["size"]
                ):
                    for key, value in color_size_update.items():
                        setattr(product_variations_base_data, key, value)

        new_product_store: ProductModel = ProductModel(
            **{**product.asdict(), "id_store": data["id_store"]}
        )
        list_variation = [element.asdict() for element in product.variations]

        list_instance_variavel = [
            VariationModel(**element) for element in list_variation
        ]

        new_product_store.variations = list_instance_variavel

        session.add(new_product_store)
        session.commit()

        return jsonify(new_product_store), HTTPStatus.CREATED
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except BodyNoContent as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


def get_all_products_for_store(id: int):
    products = ProductModel.query.filter_by(id_store=id).all()
    return jsonify(products), HTTPStatus.OK
