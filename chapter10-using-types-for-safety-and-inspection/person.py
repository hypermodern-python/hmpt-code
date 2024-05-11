from typing import Any, TypedDict

from typeguard import check_type


class Person(TypedDict):
    name: str
    age: int

    @classmethod
    def check(cls, data: Any) -> "Person":
        return check_type(data, Person)
