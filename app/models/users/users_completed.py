from dataclasses import dataclass

from sqlalchemy.sql.sqltypes import DateTime


@dataclass
class UsersCompletedModel:

    id_user: int
    user_name: str
    password: str
    id_type_user: int
    name_type_user: str
    permission: int
    id_seller: int
    first_name: str
    last_name: str
    id_store: int
    date_creation: DateTime

    @classmethod
    def separates_model(
        cls,
        list_keys_users: list[str],
        list_keys_type_user: list[str],
        list_keys_seller: list[str],
        data_json: dict,
    ) -> dict:
        user = {}
        type_user = {}
        seller = {}
        id_store = {}
        for key, value in data_json.items():
            if key in list_keys_users:
                user[key] = value
            if key in list_keys_type_user:
                type_user[key] = value
            if key in list_keys_seller:
                seller[key] = value
            data: dict = {
                "user": user,
                "type_user": type_user,
                "seller": seller,
                "id_store": id_store,
            }
        return data
