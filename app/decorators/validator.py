import datetime
from functools import wraps
from http import HTTPStatus as httpstatus

from app.helpers import get_data
from re import match


def validator(
    user_name: str = None,
    date: str = None,
    phone: str = None,
    cpf: str = None,
    zip_code: str = None,
    email=None,
    password=None,
    birthdate: str = None,
):
    def received_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            regex_bithdate = (
                "^(0[1-9]|[12][0-9]|3[01])[\/\-](0[1-9]|1[012])[\/\-]\d{4}$"
            )
            regex_phone = "^\([1-9]{2}\)(?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$"
            regex_cep = "^[0-9]{5}-[0-9]{3}$"
            regex_cpf = "^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\.?[0-9]{2}$"
            regex_email = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"
            regex_name = "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s]+$"
            regex_password = "^((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$"

            request_json: dict = get_data()

            if request_json.get(date):
                date_now = datetime.date.today()
                date_passed = request_json[date]

                if not date_now >= date_passed:
                    return {"error": "that date has passed"}, httpstatus.BAD_REQUEST

            if request_json.get(birthdate):
                if not match(regex_bithdate, request_json[birthdate]):
                    return {
                        "error": "birthdate in format incorrect"
                    }, httpstatus.BAD_REQUEST

            if request_json.get(phone):
                if not match(regex_phone, request_json[phone]):
                    return {
                        "error": "phone in format incorrect"
                    }, httpstatus.BAD_REQUEST

            if request_json.get(cpf):
                if not match(regex_cpf, request_json[cpf]):
                    return {"error": "cpf in format incorrect"}, httpstatus.BAD_REQUEST

            if request_json.get(zip_code):
                if not match(regex_cep, request_json[zip_code]):
                    return {"error": "cep in format incorrect"}, httpstatus.BAD_REQUEST

            if request_json.get(email):
                if not match(regex_email, request_json[email]):
                    return {
                        "error": "email in format incorrect"
                    }, httpstatus.BAD_REQUEST

            if request_json.get(password):
                if not match(regex_password, request_json[password]):
                    return {
                        "error": "password in format incorrect",
                        "should be": "Password must contain at least one letter uppercase, one lowercase, one number and one special character",
                    }, httpstatus.BAD_REQUEST

            if request_json.get(user_name):
                if not match(regex_name, request_json[user_name]):
                    return {"error": "name in format incorrect"}, httpstatus.BAD_REQUEST

            return function(*args, **kwargs)

        return wrapper

    return received_function
