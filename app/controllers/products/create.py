from flask import current_app, jsonify
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.decorators import verify_payload

from app.models.product.product_completed import ProductCompletedModel
from app.models.product.products_model import ProductModel
from app.models.product.variation_model import VariationModel

from app.helpers import get_files


@verify_payload(
    fields_and_types={
        "id_category": int,
        "name": str,
        "variations": list,
        "quantity_atacado": int,
        "cost_value": [int, float],
        "sale_value_atacado": [int, float],
        "sale_value_varejo": [int, float],
        "id_store": int,
        "sale_value_promotion": [int, float],
        "date_start": str,
        "date_end": str,
    },
    optional=["sale_value_promotion", "start", "end"],
)
def create_product(data: dict):
    session: Session = current_app.db.session
    try:
        keys_product = [
            "name",
            "cost_value",
            "sale_value_varejo",
            "sale_value_atacado",
            "id_category",
            "quantity_atacado",
            "id_store",
            "sale_value_promotion",
            "date_start",
            "date_end",
        ]
        keys_colors = ["variations", "color_name"]
        keys_sizes_product = ["sizes_product"]

        product, colors_sizes_product = ProductCompletedModel.separates_model(
            keys_product, keys_colors, keys_sizes_product, data
        ).values()

        new_product = ProductModel(**product)
        new_product.variations = [
            VariationModel(**{**element, "id_product": new_product.id_product})
            for element in colors_sizes_product
        ]

        files = get_files()

        if files:
            for file in files:
                new_product.image = file.file_bin
                new_product.image_mimeType = file.mimetype
                new_product.image_name = file.filename
        print("PRODUCT: ", new_product)
        session.add(new_product)
        session.commit()

        return jsonify(new_product), HTTPStatus.CREATED
    except AttributeError:
        return {"erro": "atribute error pesquisar"}, HTTPStatus.NOT_FOUND
    except IntegrityError as e:
        return {"erro": f"{e.args[0]} "}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
