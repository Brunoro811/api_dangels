from flask import current_app, request
from http import HTTPStatus as httpstatus

from app.models.category_products.category_model import CategoryModel

from sqlalchemy.orm import Session


def update_category(id_category: int):
    try:
        session: Session = current_app.db.session
        data: dict = request.get_json()
        name = data["name"]

        if len(list(data.values())) > 1:
            return {
                "error": "must only count name key!"
            }, httpstatus.UNPROCESSABLE_ENTITY

        category = CategoryModel.query.get(id_category)
        setattr(category, "name", name)

        session.add(category)
        session.commit()
        return "", httpstatus.NO_CONTENT
    except AttributeError:
        return {"error": "category not found!"}, httpstatus.NOT_FOUND
    except Exception as e:
        raise e
