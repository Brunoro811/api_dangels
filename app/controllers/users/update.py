from flask import current_app, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.controllers.exc.user_erros import (
    BodyNoContent,
    TypeSellerInvalid,
)
from app.helpers import get_data

from app.models.users.users_completed import UsersCompletedModel
from app.models.users.seller_model import SellerModel
from app.models.users.users_model import UsersModel


from app.controllers.decorators import (
    verify_keys,
    verify_types,
    validator,
)


def update_users(id: int):
    session: Session = current_app.db.session
    try:
        if not (request.get_json()):
            raise BodyNoContent("body invalid, JSON not found!")
        data2 = get_data()
        data = request.get_json()

        user: UsersModel = UsersModel.query.get(id)
        if not user:
            raise NoResultFound

        print("")
        print("user: ", user)
        print("")

        # seller = SellerModel.query.get(id)

        list_keys_user = ["user_name", "password"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        new_data = UsersCompletedModel.separates_model(
            list_keys_user, lsit_keys_seller, data
        )
        """

        if new_data.get("user"):
            for key, value in new_data["user"].items():
                setattr(user, key, value)

        if new_data.get("seller"):
            for key, value in new_data["seller"].items():
                setattr(seller, key, value)
            user.sellers = seller
        user.sellers = seller
        session.add(user)
        session.commit()"""

        return "", HTTPStatus.NO_CONTENT
    except TypeSellerInvalid as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except BodyNoContent as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
