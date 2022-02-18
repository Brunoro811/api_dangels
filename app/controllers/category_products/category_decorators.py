from functools import wraps
from http import HTTPStatus as httpstatus

from flask import request


def verify_category(func):
    @wraps(func)
    def wrapper():
        try:
            data: dict = request.get_json()
            name = data["name"]
            if len(list(data.values())) > 1:
                return {
                    "erro": "must only count name key!"
                }, httpstatus.UNPROCESSABLE_ENTITY
            if type(name) != str:
                raise TypeError
            return func()
        except KeyError:
            return {"erro": "key name missing!"}, httpstatus.UNPROCESSABLE_ENTITY
        except TypeError:
            return {
                "erro": "key name should be string!"
            }, httpstatus.UNPROCESSABLE_ENTITY
        except Exception as e:
            raise e

    return wrapper
