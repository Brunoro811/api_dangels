from pickletools import optimize
from flask import current_app, jsonify, request, Response
from http import HTTPStatus
from PIL import Image
import json

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
from sqlalchemy.exc import IntegrityError

from werkzeug.exceptions import BadRequestKeyError
from werkzeug.utils import secure_filename


from app.controllers.products.products_helpers import help_normalize_variations
from app.models.product.group_model import GroupModel
from app.models.product.product_completed import ProductCompletedModel
from app.models.product.products_model import ProductModel
from app.models.product.variation_model import VariationModel

from app.controllers.decorators import verify_keys, verify_types, validator


@verify_keys(
    [
        "cost_value",
        "id_category",
        "id_store",
        "name",
        "quantity_atacado",
        "sale_value_atacado",
        "sale_value_varejo",
        "variations",
        # "sale_value_promotion",
        # "date_start",
        # "date_end",
    ]
)
@verify_types(
    {
        "id_category": int,
        "name": str,
        "variations": list,
        "quantity_atacado": int,
        "cost_value": [int, float],
        "sale_value_atacado": [int, float],
        "sale_value_varejo": [int, float],
        "id_store": int,
        # "sale_value_promotion": float,
        # "date_start": str,
        # "date_end": str,
    }
)
# @validator(date="date_start")
# @validator(date="date_end")
def create_product():
    session: Session = current_app.db.session
    try:
        keys_product = [
            "name",
            "cost_value",
            "sale_value_varejo",
            "sale_value_atacado",
            # "sale_value_promotion",
            "id_category",
            "quantity_atacado",
            "id_store",
            "file",
        ]
        keys_colors = ["variations", "color_name"]
        keys_sizes_product = ["sizes_product"]

        data = None

        if request.get_json():
            data = request.get_json()
        else:
            data: dict = json.loads(request.form.get("product"))
            data.pop("file")

        obj_product_completed = ProductCompletedModel.separates_model(
            keys_product, keys_colors, keys_sizes_product, data
        )
        product = dict(obj_product_completed["product"])
        new_product = ProductModel(**product)

        if request.files:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            mimetype = file.mimetype
            new_product.image = file.read()
            new_product.image_mimeType = mimetype
            new_product.image_name = filename

        list_colors_sizes = [*obj_product_completed["colors_sizes_product"]]

        new_product.variations = [
            VariationModel(**{**element, "id_product": new_product.id_product})
            for element in list_colors_sizes
        ]

        session.add(new_product)
        session.commit()

        return jsonify(data), HTTPStatus.CREATED
    except AttributeError:
        return {"erro": "atribute error pesquisar"}, HTTPStatus.NOT_FOUND
    except IntegrityError as e:
        return {"erro": f"{e.args[0]} "}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


def create_images_product(id: int):
    try:
        session: Session = current_app.db.session
        product: ProductModel = ProductModel.query.get(id)
        if not product:
            raise NoResultFound

        file = request.files["file"]
        filename = secure_filename(file.filename)
        mimetype = file.mimetype

        product.image = file.read()
        product.image_mimeType = mimetype
        product.image_name = filename

        session.add(product)
        session.commit()

        return jsonify(""), HTTPStatus.CREATED
    except BadRequestKeyError:
        return {"error": "File not found"}, HTTPStatus.NOT_FOUND
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def get_image_product(name: str):
    try:
        product: ProductModel = ProductModel.query.filter_by(image_name=name).first()
        if not product:
            return {"error": "not found image"}, HTTPStatus.NOT_FOUND

        return Response(product.image, mimetype=product.image_mimeType)
    except Exception as e:
        raise e


def get_product():
    product_list: ProductModel = ProductModel.query.all()

    return jsonify(product_list), HTTPStatus.OK


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


def get_all_product_completed():
    product_list: ProductModel = ProductModel.query.all()
    product_list_completed = []
    for product in product_list:
        product: ProductModel
        product_completed = {}
        product_completed = {**product.asdict(), **product.store.asdict()}
        product_list_completed.append(product_completed)

    return jsonify(product_list_completed), HTTPStatus.OK


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


@verify_keys(
    [
        "id_product_one",
        "id_product_two",
    ]
)
@verify_types(
    {
        "id_product_one": int,
        "id_product_two": int,
    }
)
def create_group():
    try:
        session: Session = current_app.db.session
        data: dict = request.get_json()
        ids_products = list(data.values())
        for id in ids_products:
            product = ProductModel.query.get(id)
            if not product:
                raise NoResultFound
        group = GroupModel(
            **{
                "id_product_one": ids_products[0],
                "id_product_two": ids_products[1],
            }
        )
        session.add(group)
        session.commit()

        return jsonify(group), HTTPStatus.CREATED
    except IntegrityError:
        return {"error": "Group already exist!"}, HTTPStatus.NOT_FOUND
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def get_groups():
    try:

        groups = GroupModel.query.all()
        #        print("groups -> ", dir(groups))

        return jsonify(groups), HTTPStatus.CREATED
    except Exception as e:
        raise e
