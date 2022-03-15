from flask import current_app
from http import HTTPStatus


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


from app.models.product.products_model import ProductModel
from app.models.product.variation_model import VariationModel


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
