from flask import jsonify
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound

from app.models.users.users_model import UsersModel


def get_one_users(id: int):
    try:
        user: UsersModel = UsersModel.query.get(id)
        if not (user):
            raise NoResultFound

        return jsonify(user), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
