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
