from flask import current_app
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.product.product_completed import ProductCompletedModel
from app.models.product.products_model import ProductModel


from app.controllers.decorators import verify_keys, verify_types

from app.helpers.get_data_json_multi_part_form import get_data, get_files


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
        data = get_data()

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