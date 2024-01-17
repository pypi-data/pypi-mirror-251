from enum import Enum


class User(object):
    class UType(Enum):
        UTypeSystem = 1
        UTypeAdmin = 2
        UTypeUser = 3

    def __init__(self, name: str, auth: str, u_type: UType = UType.UTypeUser):
        self.name = name
        self.auth = auth
        self.u_type = u_type

    def __str__(self) -> str:
        return f'User:{{ name:{self.name},auth: {self.auth},u_type: {self.u_type}}}'

    def to_dict(self) -> dict:
        return {"name": self.name, "auth": self.auth, "u_type": self.u_type.value}

    @staticmethod
    def keys() -> tuple:
        return "name", "auth", "u_type"

    def __getitem__(self, item: str) -> str:
        return getattr(self, item)
