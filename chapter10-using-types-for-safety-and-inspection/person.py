import json
from pathlib import Path
from typing import Any, TypedDict

import typeguard
from typeguard import check_type, typechecked, CollectionCheckStrategy


typeguard.config.collection_check_strategy = CollectionCheckStrategy.ALL_ITEMS


class Person(TypedDict):
    name: str
    age: int

    @classmethod
    def check(cls, data: Any) -> "Person":
        return check_type(data, Person)


@typechecked
def load_people(path: Path) -> list[Person]:
    with path.open() as io:
        return json.load(io)
