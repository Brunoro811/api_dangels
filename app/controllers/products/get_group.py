from flask import jsonify
from http import HTTPStatus


from app.models.group_products.group_model import GroupModel


def get_groups_products():
    try:
        groups = GroupModel.query.all()

        return jsonify(groups), HTTPStatus.CREATED
    except Exception as e:
        raise e
