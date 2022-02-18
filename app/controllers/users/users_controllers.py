from flask import current_app, jsonify, request
from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


from app.models.users.users_completed import UsersCompletedModel
from app.models.users.type_user_model import TypeUserModel
from app.models.users.seller_model import SellerModel
from app.models.users.users_model import UsersModel

from app.controllers.decorators import verify_keys, verify_optional_keys, verify_types


"""@verify_keys(
    [
        "email",
        "first_name",
        "id_store",
        "last_name",
        "name_type_user",
        "password",
        "permission",
        "user_name",
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
)"""


def create_users():
    try:

        session: Session = current_app.db.session
        data = request.get_json()

        list_keys_user = ["user_name", "password", "email"]
        list_keys_type_user = ["name_type_user", "permission"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        data = UsersCompletedModel.separates_model(
            list_keys_user, list_keys_type_user, lsit_keys_seller, data
        )

        new_type_user = TypeUserModel(**data["type_user"])
        session.add(new_type_user)

        new_seller = SellerModel(**data["seller"])
        session.add(new_seller)
        session.commit()

        new_user = UsersModel(
            **{
                **data["user"],
                "id_type_user": new_type_user.id_type_user,
                "id_seller": new_seller.id_seller,
            }
        )
        print("TYpeUser=>", new_type_user)
        print("new_seller=>", new_seller)
        print("new_user=>", new_user)
        session.add(new_user)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except IntegrityError:
        return {"error": "Store not found or not created!"}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


@verify_optional_keys(
    [
        "first_name",
        "id_store",
        "last_name",
        "name_type_user",
        "password",
        "permission",
        "user_name",
    ]
)
def update_users(id: int):
    session: Session = current_app.db.session
    try:
        user = UsersModel.query.get(id)
        if not user:
            raise NoResultFound
        type_user = TypeUserModel.query.get(id)
        seller = SellerModel.query.get(id)

        data = request.get_json()

        list_keys_user = ["user_name", "password"]
        list_keys_type_user = ["name_type_user", "permission"]
        lsit_keys_seller = ["first_name", "last_name", "id_store"]

        new_data = UsersCompletedModel.separates_model(
            list_keys_user, list_keys_type_user, lsit_keys_seller, data
        )

        if new_data["user"]:
            for key, value in new_data["user"].items():
                setattr(user, key, value)

        if new_data["type_user"]:
            for key, value in new_data["type_user"].items():
                setattr(type_user, key, value)

        if new_data["seller"]:
            for key, value in new_data["seller"].items():
                setattr(seller, key, value)

        session.add(user)
        session.add(type_user)
        session.add(seller)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
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
        session.delete(type_user)
        session.delete(user)
        session.commit()

    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

    return ""


def get_users():
    users = UsersModel.query.all()
    type_users = TypeUserModel.query.all()
    sellers = SellerModel.query.all()

    list_users = []
    count = 0
    for user in users:
        list_users.append(
            UsersCompletedModel(
                **{
                    **user.__asdict__(),
                    **type_users[count].__asdict__(),
                    **sellers[count].__asdict__(),
                }
            )
        )
        count += 1

    return jsonify(list_users), HTTPStatus.OK


def get_one_users(id: int):
    try:
        user = UsersModel.query.get(id)
        if not (user):
            raise NoResultFound

        type_user = TypeUserModel.query.get(id)
        seller = SellerModel.query.get(id)
        user_completed = UsersCompletedModel(
            **{
                **user.__asdict__(),
                **type_user.__asdict__(),
                **seller.__asdict__(),
            }
        )
    except NoResultFound:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

    return jsonify(user_completed), HTTPStatus.OK
