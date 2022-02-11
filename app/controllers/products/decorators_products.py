from functools import wraps
from http import HTTPStatus as httpstatus

from flask import request

def verify_keys(correct_keys: list[str]):
    def received_function(function):
        @wraps(function)
        def wrapper():
            request_json: dict = request.get_json()
            lista_keys_received = list(request_json.keys())
            lista_keys_received.sort()
            correct_keys.sort()
            try:
                count = 0
                if len(correct_keys) > len(lista_keys_received):
                    return {"error": "some keys is missing!"}, 400
                if len(correct_keys) < len(lista_keys_received):
                    return {"error": "some keys is left over!"}, 400
                for key in lista_keys_received:
                    if not key == correct_keys[count]:
                        raise KeyError
                    count += 1
                return function()
            except KeyError:
                return {
                    "error": "key(s) incorrect",
                    "expected": correct_keys,
                    "received": list(request_json.keys())
                }, 400
        return wrapper
    return received_function

def verify_types(correct_types: dict):
    def received_function(function):
        @wraps(function)
        def wrapper():
            data: dict = request.get_json()
            try:
                key_error = []
                for key,value in correct_types.items():
                    if ( type(data[key]) != value ):
                        print(f"{key}-> {type(data[key])} value-> {value}")
                        key_error.append(data[key])
                if(key_error):
                    raise TypeError
         
                return function()
            except TypeError:
                return {
                    "erro": "tipo de campo incorreto. deveria",
                    "Recedido com tipo errado": key_error 
                    },httpstatus.UNPROCESSABLE_ENTITY
            except Exception as e:
                raise e
        return wrapper
    return received_function

def verify_optional_keys(expected_keys: list):
    def received_func_path(func):
        @wraps(func)
        def wrapper(id_product):
            request_json: dict = request.get_json()
            request_json_keys = sorted(list(request_json.keys()))
            try:
                key_error = []
                count = 0
                for element in request_json_keys:
                    print("ELEMENT=>",element)
                    if not element in expected_keys:
                        key_error.append(request_json_keys[count])
                    count += 1
                if key_error:
                    raise KeyError
                return func(id_product)
            except KeyError as e:
                return {
                    "available_keys": expected_keys,
                    "wrong_keys_sended": key_error,
                }, 422
            except Exception as e:
                raise e

        return wrapper

    return received_func_path