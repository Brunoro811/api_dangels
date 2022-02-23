from functools import wraps
from http import HTTPStatus as httpstatus

from flask import request
from re import match

from app.controllers.exc.user_erros import UserInvalid


def verify_keys(expected_keys: list, optional_keys: bool = False):
    def received_func_path(func):
        @wraps(func)
        def wrapper(id: int = 0):
            request_json: dict = request.get_json()
            request_json_keys = sorted(list(request_json.keys()))
            request_json_keys.sort()
            expected_keys.sort()
            try:

                key_error = []
                count = 0

                if optional_keys:
                    for element in request_json_keys:
                        if not element in expected_keys:
                            key_error.append(request_json_keys[count])
                        count += 1
                else:
                    if len(expected_keys) > len(request_json_keys):
                        return {
                            "error": "some keys is missing!"
                        }, httpstatus.UNPROCESSABLE_ENTITY
                    if len(expected_keys) < len(request_json_keys):
                        return {
                            "error": "some keys is left over!"
                        }, httpstatus.UNPROCESSABLE_ENTITY

                    for key in request_json_keys:
                        if not key == expected_keys[count]:
                            key_error.append(key)
                        count += 1

                if key_error:
                    raise KeyError
                if id:
                    return func(id)
                return func()

            except KeyError as e:
                return {
                    "available_keys": expected_keys,
                    "wrong_keys_sended": key_error,
                }, 422
            except Exception as e:
                raise e

        return wrapper

    return received_func_path


def verify_types(correct_types: dict, optional_keys: bool = False):
    def received_function(function):
        @wraps(function)
        def wrapper(id: int = None):
            data: dict = request.get_json()
            try:
                key_error = []
                if not (optional_keys):
                    for key, value in correct_types.items():
                        if type(data[key]) != value:
                            key_error.append(data[key])
                else:
                    for key, value in correct_types.items():
                        if not (data.get(key, None) == None):
                            if type(data[key]) != value:
                                key_error.append(data[key])

                if key_error:
                    raise TypeError
                if not id:
                    return function()
                return function(id)
            except TypeError:
                return {
                    "error": "value with type incorrect!",
                    "received wrong": key_error,
                }, httpstatus.UNPROCESSABLE_ENTITY
            except Exception as e:
                raise e

        return wrapper

    return received_function


def verify_keys_list_interna_one(name_list: str, correct_keys: list[str]):
    def received_function(function):
        @wraps(function)
        def wrapper():
            request_json: dict = request.get_json()
            request_json = request_json[name_list]
            correct_keys.sort()
            try:
                for element in request_json:
                    lista_keys_received = list(element.keys())
                    count = 0
                    key_error = []
                    if len(correct_keys) > len(lista_keys_received):
                        return {
                            "error": "some keys is missing!"
                        }, httpstatus.UNPROCESSABLE_ENTITY
                    if len(correct_keys) < len(lista_keys_received):
                        return {
                            "error": "some keys is left over!"
                        }, httpstatus.UNPROCESSABLE_ENTITY
                    for key in element:
                        if not key in correct_keys:
                            key_error.append(key)
                        count += 1
                    if key_error:
                        raise KeyError

                return function()
            except KeyError:
                return {
                    "error": "key(s) incorrect",
                    "expected": correct_keys,
                    "received": key_error,
                }, httpstatus.UNPROCESSABLE_ENTITY

        return wrapper

    return received_function


def validate_register_user(function):
    @wraps(function)
    def wrapper(id: int = 0):
        regex_password = "^((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$"
        regex_name = "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s]+$"
        regex_email = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"

        request_json: dict = request.get_json()
        if request_json.get("user_name"):
            if not match(regex_name, request_json["user_name"]):
                return {"error": "user_name in format incorrect"}, 400
        if request_json.get("password"):
            if not match(regex_password, request_json["password"]):
                return {
                    "error": "password in format incorrect",
                    "should be": "Password must contain at least one letter uppercase, one lowercase, one number and one special character",
                }, 400
        if request_json.get("email"):
            if not match(regex_email, request_json["email"]):
                return {"error": "email in format incorrect"}, 400

        if id:
            return function(id)
        return function()

    return wrapper


def validate_register_client(function):
    @wraps(function)
    def wrapper(id: int = 0):
        regex_bithdate = "^(0[1-9]|[12][0-9]|3[01])[\/\-](0[1-9]|1[012])[\/\-]\d{4}$"
        regex_phone = "^\([1-9]{2}\)(?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$"
        regex_cep = "^[0-9]{5}-[0-9]{3}$"
        regex_cpf = "^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\.?[0-9]{2}$"
        regex_email = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"

        request_json: dict = request.get_json()

        if request_json.get("birthdate"):
            if not match(regex_bithdate, request_json["birthdate"]):
                return {"error": "birthdate in format incorrect"}, 400

        if request_json.get("phone"):
            if not match(regex_phone, request_json["phone"]):
                return {"error": "phone in format incorrect"}, 400

        if request_json.get("cpf"):
            if not match(regex_cpf, request_json["cpf"]):
                return {"error": "cpf in format incorrect"}, 400

        if request_json.get("cep"):
            if not match(regex_cep, request_json["cep"]):
                return {"error": "cep in format incorrect"}, 400

        if request_json.get("email"):
            if not match(regex_email, request_json["email"]):
                return {"error": "email in format incorrect"}, 400

        if id:
            return function(id)
        return function()

    return wrapper


def validator(
    user_name: str = None,
    date: str = None,
    phone: str = None,
    cpf: str = None,
    zip_code: str = None,
    email=None,
    password=None,
):
    def received_function(function):
        @wraps(function)
        def wrapper(id: int = 0):

            regex_bithdate = (
                "^(0[1-9]|[12][0-9]|3[01])[\/\-](0[1-9]|1[012])[\/\-]\d{4}$"
            )
            regex_phone = "^\([1-9]{2}\)(?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$"
            regex_cep = "^[0-9]{5}-[0-9]{3}$"
            regex_cpf = "^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\.?[0-9]{2}$"
            regex_email = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"
            regex_name = "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s]+$"
            regex_password = "^((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$"

            request_json: dict = request.get_json()

            if request_json.get("birthdate"):
                if not match(regex_bithdate, request_json["birthdate"]):
                    return {"error": "birthdate in format incorrect"}, 400

            if request_json.get(phone):
                if not match(regex_phone, request_json[phone]):
                    return {"error": "phone in format incorrect"}, 400

            if request_json.get(cpf):
                if not match(regex_cpf, request_json[cpf]):
                    return {"error": "cpf in format incorrect"}, 400

            if request_json.get(zip_code):
                if not match(regex_cep, request_json[zip_code]):
                    return {"error": "cep in format incorrect"}, 400

            if request_json.get(email):
                if not match(regex_email, request_json[email]):
                    return {"error": "email in format incorrect"}, 400

            if request_json.get(password):
                if not match(regex_password, request_json[password]):
                    return {
                        "error": "password in format incorrect",
                        "should be": "Password must contain at least one letter uppercase, one lowercase, one number and one special character",
                    }, 400

            if request_json.get(user_name):
                if not match(regex_name, request_json[user_name]):
                    return {"error": "name in format incorrect"}, 400

            if id:
                return function(id)
            return function()

        return wrapper

    return received_function
