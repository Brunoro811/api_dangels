from jwt.exceptions import InvalidSignatureError


class UserInvalid(Exception):
    ...


class TypeSellerInvalid(Exception):
    def __init__(self, *args: object, describe: str = "type seller not found!") -> None:
        super().__init__(*args)
        self.describe = describe
        self.status_code = 400


class BodyNoContent(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)


class TokenInvalid(Exception):
    def __init__(self, *args: object, describe: str = "Token is invalid!") -> None:
        super().__init__(*args)
        self.describe = describe


class TokenNotFound(Exception):
    def __init__(self, *args: object, describe: str = "Token not found!") -> None:
        super().__init__(*args)
        self.describe = describe
        self.status_code = 401


class UserUnauthorized(Exception):
    def __init__(self, *args: object, describe: str = "user not authorized!") -> None:
        super().__init__(*args)
        self.describe = describe
        self.status_code = 401


class StoreNotFound(Exception):
    def __init__(self, *args: object, describe: str = "Store not found!") -> None:
        super().__init__(*args)
        self.describe = describe
        self.status_code = 400


class FileNotFound(Exception):
    def __init__(self, *args: object, describe: str = "File not found!") -> None:
        super().__init__(*args)
        self.describe = describe
        self.status_code = 400
