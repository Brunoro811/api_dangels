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
                    "erro": "deve conter somente a chave name!"
                }, httpstatus.UNPROCESSABLE_ENTITY
            if type(name) != str:
                raise TypeError
            return func()
        except KeyError:
            return {"erro": "chave name faltando!"}, httpstatus.UNPROCESSABLE_ENTITY
        except TypeError:
            return {
                "erro": "chave name deve ser uma string!"
            }, httpstatus.UNPROCESSABLE_ENTITY
        except Exception as e:
            raise e

    return wrapper
