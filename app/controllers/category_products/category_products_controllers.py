from flask import current_app, jsonify, request
from http import HTTPStatus as httpstatus

from app.controllers.category_products.category_decorators import verify_category
from app.models.category_products.category_model import CategoryModel

from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
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


def get_all_category():
    try:
        categorys = CategoryModel.query.all()
        return jsonify(categorys), httpstatus.OK
    except Exception as e:
        raise e


def get_category(id_category: int):
    try:
        category = CategoryModel.query.get(id_category)
        if not category:
            raise NoResultFound

        return jsonify(category), httpstatus.OK
    except NoResultFound:
        return {"error": "Not found category."}, httpstatus.NOT_FOUND
    except Exception as e:
        raise e


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


def deleteategory(id_category: int):
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
