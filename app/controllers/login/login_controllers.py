from http import HTTPStatus
from flask import jsonify, request

from sqlalchemy.orm.exc import NoResultFound

from app.controllers.exc.user_erros import BodyNoContent
from app.models.users.users_model import UsersModel

from app.auth import token_creator


def create_login():
    try:
        if not request.get_json():
            raise BodyNoContent("JSON no content!")
        data = request.get_json()

        found_user: UsersModel = UsersModel.query.filter_by(
            user_name=data["user_name"]
        ).first()

        if not found_user:
            raise NoResultFound

        if not found_user.verify_password(data["password"]):
            raise NoResultFound

        token = token_creator.create(uid=1)

        return (
            jsonify(
                {
                    **found_user.asdict(),
                    "token": token,
                }
            ),
            HTTPStatus.OK,
        )
    except NoResultFound as e:
        return {"error": f"user_name or password invalid!"}, HTTPStatus.UNAUTHORIZED
    except BodyNoContent as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
