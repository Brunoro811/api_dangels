from flask import current_app, jsonify, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from app.controllers.exc.user_erros import BodyNoContent, TypeSellerInvalid


from app.models.users.users_completed import UsersCompletedModel
from app.models.users.type_user_model import TypeUserModel
from app.models.users.seller_model import SellerModel
from app.models.users.users_model import UsersModel

from app.controllers.decorators import validate_register_user, verify_keys, verify_types


@verify_keys(
    [
        "user_name",
        "password",
        "name_type_user",
        "permission",
        "first_name",
        "last_name",
        "id_store",
        "email",
    ]
)
@verify_types(
    {
        "email": str,
        "first_name": str,
        "id_store": int,
        "last_name": str,
        "name_type_user": str,
        "password": str,
        "permission": int,
        "user_name": str,
    }
)
@validate_register_user
def create_users():
    try:

        session: Session = current_app.db.session
        data = request.get_json()

        name_type_user: TypeUserModel = TypeUserModel.query.filter_by(
            name_type_user=data["name_type_user"]
        ).first()
        if not name_type_user:
            raise TypeSellerInvalid("Type seller invalid or not register!")

        list_keys_user = ["user_name", "password", "email"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        data = UsersCompletedModel.separates_model(
            list_keys_user, lsit_keys_seller, data
        )

        new_seller = SellerModel(**data["seller"])
        new_user: UsersModel = UsersModel(**data["user"])
        new_user.sellers = new_seller
        new_user.types_users = name_type_user

        session.add(new_user)
        session.commit()

        user_completed = {
            **new_user.asdict(),
            **new_user.sellers.asdict(),
            **new_user.types_users.asdict(),
        }
        return jsonify(user_completed), HTTPStatus.CREATED
    except TypeSellerInvalid as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {"error": "user already exist!"}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


@verify_keys(
    [
        "first_name",
        "id_store",
        "last_name",
        "name_type_user",
        "password",
        "permission",
        "user_name",
    ],
    optional_keys=True,
)
@validate_register_user
def update_users(id: int):
    session: Session = current_app.db.session
    try:
        if not (request.get_json()):
            raise BodyNoContent("body invalid, JSON not found!")
        data = request.get_json()

        user: UsersModel = UsersModel.query.get(id)
        if not user:
            raise NoResultFound
        seller = SellerModel.query.get(id)

        list_keys_user = ["user_name", "password"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        new_data = UsersCompletedModel.separates_model(
            list_keys_user, lsit_keys_seller, data
        )

        if new_data.get("user"):
            for key, value in new_data["user"].items():
                setattr(user, key, value)

        if new_data.get("seller"):
            for key, value in new_data["seller"].items():
                setattr(seller, key, value)
            user.sellers = seller
        user.sellers = seller
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


def get_users():
    users = UsersModel.query.all()

    list_users = []
    for user in users:
        list_users.append(
            UsersCompletedModel(
                **{
                    **user.sellers.asdict(),
                    **user.types_users.asdict(),
                    **user.asdict(),
                }
            )
        )

    return jsonify(list_users), HTTPStatus.OK


def get_one_users(id: int):
    try:
        user: UsersModel = UsersModel.query.get(id)
        if not (user):
            raise NoResultFound
        user_completed = UsersCompletedModel(
            **{**user.sellers.asdict(), **user.types_users.asdict(), **user.asdict()}
        )
        return jsonify(user_completed), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
