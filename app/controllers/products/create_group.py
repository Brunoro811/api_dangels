from flask import current_app, jsonify, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


from app.models.product.group_model import GroupModel
from app.models.product.products_model import ProductModel

from app.controllers.decorators import verify_keys, verify_types


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
def create_group_products():
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
