from flask import current_app
from http import HTTPStatus as httpstatus

from app.models.category_products.category_model import CategoryModel

from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm import Session


def delete_category(id_category: int):
    try:
        session: Session = current_app.db.session
        category = CategoryModel.query.get(id_category)
        session.delete(category)
        session.commit()
        return "", httpstatus.NO_CONTENT
    except UnmappedInstanceError:
        return {"error": "category not found!"}, httpstatus.NOT_FOUND
    except Exception as e:
        raise e
