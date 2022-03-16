from flask import current_app
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.users.users_model import UsersModel


def delete_users(id: int):
    try:
        session: Session = current_app.db.session
        user: UsersModel = UsersModel.query.get(id)
        if not (user):
            raise NoResultFound
        user.password_hash = ""
        session.commit()

    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

    return "", HTTPStatus.NO_CONTENT
