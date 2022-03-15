from flask import Response
from http import HTTPStatus

from app.models.product.products_model import ProductModel


def get_image_product(name: str):
    try:
        product: ProductModel = ProductModel.query.filter_by(image_name=name).first()
        if not product:
            return {"error": "not found image"}, HTTPStatus.NOT_FOUND

        return Response(product.image, mimetype=product.image_mimeType)
    except Exception as e:
        raise e
