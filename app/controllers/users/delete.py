from flask import current_app
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.users.type_user_model import TypeUserModel
from app.models.users.seller_model import SellerModel
from app.models.users.users_model import UsersModel


def delete_users(id: int):
    try:
        session: Session = current_app.db.session
        user = UsersModel.query.get(id)
        if not (user):
            raise NoResultFound
        type_user = TypeUserModel.query.get(id)
        seller = SellerModel.query.get(id)
        session.delete(seller)
        session.commit()
        session.delete(user)
        session.commit()

    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

    return ""
