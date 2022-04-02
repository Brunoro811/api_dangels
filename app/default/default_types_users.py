from flask import current_app
from sqlalchemy.orm import Session

from app.models.stores.store_model import StoreModel
from app.models.types_users.type_user_model import TypeUserModel

from app.default.default_values import type_users


def default_types_users():
    try:
        session: Session = current_app.db.session
        types_users: StoreModel = TypeUserModel.query.all()
        if not types_users:
            types_users_list = []
            for user in type_users:
                types_users_list.append(TypeUserModel(**user))
            session.add_all(types_users_list)
            session.commit()
    except Exception as e:
        raise e
