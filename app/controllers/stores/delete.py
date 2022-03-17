from flask import current_app
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.stores.store_model import StoreModel


def delete_store(id: int):
    session: Session = current_app.db.session
    try:
        store = StoreModel.query.get(id)
        if not (store):
            raise NoResultFound
        session.delete(store)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found store."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
