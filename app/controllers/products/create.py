from flask import current_app, jsonify
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.decorators import verify_payload

from app.models.product.products_model import ProductModel
from app.models.variations_products.variation_model import VariationModel

from app.helpers import get_files


@verify_payload(
    fields_and_types={
        "id_category": int,
        "name": str,
        "variations": list,
        "quantity_atacado": int,
        "cost_value": [int, float],
        "color": str,
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
        list_variation = data.pop("variations")
        product = data

        new_product = ProductModel(**product)
        new_product.variations = [
            VariationModel(**{**element, "id_product": new_product.id_product})
            for element in list_variation
        ]

        files = get_files()

        if files:
            for file in files:
                new_product.image = file.file_bin
                new_product.image_mimeType = file.mimetype
                new_product.image_name = file.filename

        session.add(new_product)
        session.commit()

        return jsonify(new_product), HTTPStatus.CREATED
    except AttributeError:
        return {"erro": "atribute error pesquisar"}, HTTPStatus.NOT_FOUND
    except IntegrityError as e:
        return {"erro": f"{e.args[0]} "}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
