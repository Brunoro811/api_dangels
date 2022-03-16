from flask import current_app, jsonify, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.controllers.exc.user_erros import (
    TypeSellerInvalid,
    StoreNotFound,
)
from app.decorators import verify_payload

from app.models.users.users_completed import UsersCompletedModel
from app.models.users.type_user_model import TypeUserModel
from app.models.users.seller_model import SellerModel
from app.models.users.users_model import UsersModel
from app.models.stores.store_model import StoreModel

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
    optional=[],
)
def create_users(data: dict):
    try:
        session: Session = current_app.db.session

        password_to_hash = data.pop("password")

        name_type_user: TypeUserModel = TypeUserModel.query.filter_by(
            name_type_user=data["name_type_user"]
        ).first()
        if not name_type_user:
            raise TypeSellerInvalid

        store: StoreModel = StoreModel.query.get(data["id_store"])
        if not store:
            raise StoreNotFound("Store not found!")

        list_keys_user = ["user_name", "email"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        data = UsersCompletedModel.separates_model(
            list_keys_user, lsit_keys_seller, data
        )

        new_user: UsersModel = UsersModel(**data["user"])
        new_user.password = password_to_hash

        new_seller = SellerModel(**data["seller"])
        new_user.sellers = new_seller
        new_user.types_users = name_type_user

        session.add(new_user)
        session.commit()

        return jsonify(new_user), HTTPStatus.CREATED
    except TypeSellerInvalid as e:
        return {"error": f"{e.describe}"}, e.status_code
    except IntegrityError:
        return {"error": "user already exist!"}, HTTPStatus.BAD_REQUEST
    except StoreNotFound as e:
        return {"error": f"{e.describe}"}, e.status_code
    except Exception as e:
        raise e
