from flask import jsonify
from http import HTTPStatus


from sqlalchemy.orm.exc import NoResultFound


from app.models.client.client_model import ClientModel


def get_one_client(id: int):
    try:
        client = ClientModel.query.get(id)
        if not client:
            raise NoResultFound
        return jsonify(client), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found client."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
