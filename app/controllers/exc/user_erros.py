class UserInvalid(Exception):
    ...


class TypeSellerInvalid(Exception):
    ...

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)


class BodyNoContent(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
