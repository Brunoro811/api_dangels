from flask import current_app, jsonify, request
from http import HTTPStatus


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
from sqlalchemy.exc import IntegrityError
from app.controllers.products.products_helpers import help_normalize_variations


from app.models.product.product_completed import ProductCompletedModel
from app.models.product.products_model import ProductModel
from app.models.product.variation_model import VariationModel

from app.controllers.decorators import verify_keys, verify_types


@verify_keys(
    [
        "cost_value",
        "id_category",
        "name",
        "sale_value_varejo",
        "variations",
        "quantity_atacado",
        "sale_value_promotion",
        "sale_value_atacado",
    ]
)
@verify_types(
    {
        "cost_value": float,
        "id_category": int,
        "name": str,
        "variations": list,
        "quantity_atacado": int,
        "sale_value_promotion": float,
        "sale_value_atacado": float,
        "sale_value_varejo": float,
    }
)
def create_product():
    session: Session = current_app.db.session
    try:
        keys_product = [
            "name",
            "cost_value",
            "sale_value_varejo",
            "sale_value_atacado",
            "sale_value_promotion",
            "id_category",
            "quantity_atacado",
        ]
        keys_colors = ["variations", "color_name"]
        keys_sizes_product = ["sizes_product"]
        data: dict = request.get_json()

        obj_product_completed = ProductCompletedModel.separates_model(
            keys_product, keys_colors, keys_sizes_product, data
        )

        product = dict(obj_product_completed["product"])
        new_product = ProductModel(**product)

        session.add(new_product)
        session.commit()

        list_colors_sizes = [*obj_product_completed["colors_sizes_product"]]

        obj_variations = [
            VariationModel(**{**element, "id_product": new_product.id_product})
            for element in list_colors_sizes
        ]

        session.add_all(obj_variations)
        session.commit()
        data["id_product"] = new_product.id_product
        return jsonify(data), HTTPStatus.CREATED
    except AttributeError:
        return {"erro": "atribute error pesquisar"}, HTTPStatus.NOT_FOUND
    except IntegrityError as e:
        return {"erro": f"{e.args[0]} "}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


def get_product():
    product_list = ProductModel.query.all()
    list_products = []

    for product in product_list:
        product: ProductModel
        obj_product_completed = {}
        obj_product_completed["product"] = product.asdict()
        obj_product_completed["variations"] = help_normalize_variations(
            product.variations
        )
        list_products.append(obj_product_completed)
    return jsonify(list_products), HTTPStatus.OK


def get_one_product(id: int):
    try:
        product = ProductModel.query.get(id)
        product: ProductModel

        obj_product_completed = {}
        obj_product_completed["product"] = product.asdict()
        obj_product_completed["variations"] = help_normalize_variations(
            product.variations
        )

        return jsonify(obj_product_completed), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


@verify_keys(
    [
        "cost_value",
        "id_category",
        "name",
        "sale_value_varejo",
        "variations",
        "quantity_atacado",
        "sale_value_promotion",
        "sale_value_atacado",
    ],
    optional_keys=True,
)
@verify_types(
    {
        "cost_value": float,
        "id_category": int,
        "name": str,
        "variations": list,
        "quantity_atacado": int,
        "sale_value_promotion": float,
        "sale_value_atacado": float,
        "sale_value_varejo": float,
    },
    optional_keys=True,
)
def update_product(id: int):
    session: Session = current_app.db.session
    try:

        data = request.get_json()

        keys_product = ["name", "id_category", "cost_value", "sale_value"]
        keys_colors = ["variations", "color_name"]
        keys_sizes_product = ["sizes_product"]

        product = ProductModel.query.get(id)
        if not (product):
            raise NoResultFound

        obj_product_completed = ProductCompletedModel.separates_model_for_update(
            keys_product, keys_colors, keys_sizes_product, data
        )

        if obj_product_completed["product"]:
            update_product = dict(obj_product_completed["product"])
            for key, value in update_product.items():
                setattr(product, key, value)

            session.add(product)
            session.commit()

        if obj_product_completed["variations"]:
            for color_size_update in obj_product_completed["variations"]:
                for product_variations_base_data in product.variations:
                    if (
                        product_variations_base_data.color == color_size_update["color"]
                        and product_variations_base_data.size
                        == color_size_update["size"]
                    ):
                        for key, value in color_size_update.items():
                            setattr(product_variations_base_data, key, value)
            session.add_all(product.variations)
            session.commit()

        return "", HTTPStatus.NO_CONTENT

    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def delete_product(id: int):
    try:
        session: Session = current_app.db.session
        product = ProductModel.query.get(id)
        variations = VariationModel.query.filter_by(id_product=id)

        variations.delete()
        session.delete(product)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except UnmappedInstanceError:
        return {"erro": "Not found product."}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
