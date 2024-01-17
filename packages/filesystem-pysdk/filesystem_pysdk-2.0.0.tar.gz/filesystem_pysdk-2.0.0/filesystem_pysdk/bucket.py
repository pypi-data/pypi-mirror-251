from enum import Enum


class Bucket(object):
    class BType(Enum):
        BTypeRead = 1
        BTypeWrite = 2
        BTypeReadWrite = 3

    def __init__(self, name: str, b_type: BType = BType.BTypeReadWrite, is_temp: bool = False):
        self.name = name
        self.b_type = b_type
        self.is_temp = is_temp

    def __str__(self) -> str:
        return f'Bucket:{{ name:{self.name}, b_type: {self.b_type}}}'

    def to_dict(self) -> dict:
        return {"name": self.name, "b_type": self.b_type.value, "is_temp": self.is_temp}

    @staticmethod
    def keys() -> tuple:
        return "name", "b_type", "is_temp"

    def __getitem__(self, item: str) -> str:
        return getattr(self, item)
