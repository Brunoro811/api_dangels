from flask import jsonify
from http import HTTPStatus
from app.models.users.users_model import UsersModel


def get_users():
    users = UsersModel.query.all()

    return jsonify(users), HTTPStatus.OK
