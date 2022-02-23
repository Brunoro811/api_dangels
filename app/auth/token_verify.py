from flask import request
import jwt
from functools import wraps
from jwt import ExpiredSignatureError, InvalidSignatureError

from app.controllers.exc.user_erros import TokenNotFound, UserUnauthorized

from app.auth.token_handler import token_creator


def verify_token(function: callable) -> callable:
    @wraps(function)
    def decorated(id: int = 0):
        try:
            token = request.headers.get("Authorization")
            uid = request.headers.get("uid")
            if not (token) or not (uid):
                raise TokenNotFound

            validate_token = token.split()[1]
            information_token = jwt.decode(
                validate_token, key="1234", algorithms="HS256"
            )
            token_uid = information_token["uid"]

            if int(token_uid) != int(uid):
                raise UserUnauthorized

            nex_token = token_creator.refresh(validate_token)

            if id:
                return function(id)
            return function()

        except TokenNotFound as e:
            return {"error": f"{e.describe}"}, e.status_code
        except UserUnauthorized as e:
            return {"error": f"{e.describe}"}, e.status_code
        except KeyError as e:
            return {"error": "Token invalid!"}, 401
        except InvalidSignatureError as e:
            return {"error": "Token invalid!"}, 401
        except ExpiredSignatureError as e:
            return {"error": "Token expired!"}, 401

    return decorated
