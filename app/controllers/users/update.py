from flask import current_app
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.controllers.exc.user_erros import (
    BodyNoContent,
    TypeSellerInvalid,
)


from app.models.users.users_completed import UsersCompletedModel
from app.models.users.seller_model import SellerModel
from app.models.users.users_model import UsersModel
from app.models.stores.store_model import StoreModel

from app.decorators import verify_payload
from app.controllers.decorators import (
    validator,
)


@validator(user_name="user_name", email="email", password="password")
@verify_payload(
    fields_and_types={
        "email": str,
        "first_name": str,
        "id_store": int,
        "last_name": str,
        "name_type_user": str,
        "user_name": str,
        "password": str,
    },
    optional=[
        "email",
        "first_name",
        "id_store",
        "last_name",
        "name_type_user",
        "user_name",
        "password",
    ],
)
def update_users(data: dict, id: int):
    session: Session = current_app.db.session
    try:

        user: UsersModel = UsersModel.query.get(id)
        if not user:
            raise NoResultFound

        if data.get("id_store"):
            store: StoreModel = StoreModel.query.get(data["id_store"])
            print("idstore:", store)
            if not store:
                return {"error": "Store not found"}, HTTPStatus.NOT_FOUND

        if data.get("name_type_user"):
            seller: SellerModel = SellerModel.query.filter_by(
                data["name_type_user"]
            ).first()
            if not seller:
                return {"error": "Seller not found"}, HTTPStatus.NOT_FOUND

        list_keys_user = ["user_name", "password", "email"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        new_data = UsersCompletedModel.separates_model(
            list_keys_user, lsit_keys_seller, data
        )

        if new_data.get("user"):
            for key, value in new_data["user"].items():
                setattr(user, key, value)

        if new_data.get("seller"):
            for key, value in new_data["seller"].items():
                setattr(user.sellers, key, value)

        session.add(user)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except TypeSellerInvalid as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except BodyNoContent as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
