from flask import current_app, jsonify, request
from http import HTTPStatus as httpstatus

from app.controllers.category_products.category_decorators import verify_category
from app.models.category_products.category_model import CategoryModel

from sqlalchemy.orm.exc import UnmappedInstanceError


@verify_category
def create_category():
    try:
        data = request.get_json()
        new_category = CategoryModel(**data)
        current_app.db.session.add(new_category)
        current_app.db.session.commit()
        return jsonify(new_category), httpstatus.CREATED

    except Exception as e:
        raise e


def get_all_category():
    try:
        categorys = CategoryModel.query.all()
        return jsonify(CategoryModel.serializer(categorys)), httpstatus.OK
    except Exception as e:
        raise e


def get_category():
    ...


def update_category(id_category: int):
    try:
        data: dict = request.get_json()
        name = data["name"]

        if len(list(data.values())) > 1:
            return {
                "erro": "deve ter somente o nome da categoria!"
            }, httpstatus.UNPROCESSABLE_ENTITY

        category = CategoryModel.query.get(id_category)
        setattr(category, "name", name)

        current_app.db.session.add(category)
        current_app.db.session.commit()
        return "", httpstatus.NO_CONTENT
    except AttributeError:
        return {"erro": "categoria não encontrada"}, httpstatus.NOT_FOUND
    except Exception as e:
        raise e


def deleteategory(id_category: int):
    try:
        category = CategoryModel.query.get(id_category)
        current_app.db.session.delete(category)
        current_app.db.session.commit()
        return "", httpstatus.NO_CONTENT
    except UnmappedInstanceError:
        return {"erro": "Categoria não encontrada!"}, httpstatus.NOT_FOUND
    except Exception as e:
        raise e
