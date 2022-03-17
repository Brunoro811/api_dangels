from flask import current_app, jsonify, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from werkzeug.exceptions import BadRequestKeyError
from werkzeug.utils import secure_filename

from app.models.product.products_model import ProductModel


def create_update_images_product(id: int):
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
