from datetime import datetime, timedelta
import time
import jwt


class TokenCreator:
    def __init__(
        self, token_keys: str, exp_time_minutes: int, refresh_time_minutes: int
    ) -> None:
        self.__TOKEN_KEY = token_keys
        self.__EXP_TIME_MIN = exp_time_minutes
        self.__REFRESH_TIME_MIN = refresh_time_minutes

    def create(self, uid: int):
        return self.__encode_token(uid)

    def refresh(self, token: str):
        information_token = jwt.decode(token, key=self.__TOKEN_KEY, algorithms="HS256")
        token_uid = information_token["uid"]
        exp_time = information_token["exp"]

        if ((exp_time - time.time()) / 60) < self.__REFRESH_TIME_MIN:
            return self.__encode_token(token_uid)
        return token

    def __encode_token(self, uid: int) -> str:
        token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(minutes=self.__EXP_TIME_MIN),
                "uid": uid,
            },
            key=self.__TOKEN_KEY,
            algorithm="HS256",
        )
        return token
