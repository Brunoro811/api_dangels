from flask import current_app, jsonify, request
from http import HTTPStatus as httpstatus

from app.controllers.category.category_decorators import verify_category
from app.models.category_products.category_model import CategoryModel

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


@verify_category
def create_category():
    try:
        session: Session = current_app.db.session
        data = request.get_json()
        new_category = CategoryModel(**data)
        session.add(new_category)
        session.commit()
        return jsonify(new_category), httpstatus.CREATED
    except IntegrityError:
        return {"error": "category already exist!"}, httpstatus.CONFLICT
    except Exception as e:
        raise e
