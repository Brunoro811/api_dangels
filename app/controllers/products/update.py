from flask import current_app
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.decorators import verify_payload

from app.models.product.products_model import ProductModel

from app.helpers.get_data_json_multi_part_form import get_files


@verify_payload(
    fields_and_types={
        "cost_value": [float, int],
        "id_category": int,
        "id_store": int,
        "name": str,
        "sale_value_varejo": [float, int],
        "variations": list,
        "quantity_atacado": int,
        "sale_value_promotion": [float, int],
        "sale_value_atacado": [float, int],
        "date_start": str,
        "date_end": str,
        "color": str,
    },
    optional=[
        "cost_value",
        "id_category",
        "id_store",
        "name",
        "sale_value_varejo",
        "variations",
        "quantity_atacado",
        "sale_value_promotion",
        "sale_value_atacado",
        "date_start",
        "date_end",
        "color",
    ],
)
def update_product(data: dict, id: int):
    session: Session = current_app.db.session
    try:

        product: ProductModel = ProductModel.query.get(id)
        if not (product):
            raise NoResultFound

        if data["variations"]:
            key = None
            value = None
            list_variations = data.pop("variations")

            for number_item in range(0, len(list_variations)):
                for key, value in list_variations[number_item].items():
                    setattr(product.variations[number_item], key, value)

        if data:
            for key, value in data.items():
                setattr(product, key, value)

        files = get_files()
        if files:
            for file in files:
                product.image = file.file_bin
                product.image_name = file.filename
                product.image_mimetype = file.mimetype
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
