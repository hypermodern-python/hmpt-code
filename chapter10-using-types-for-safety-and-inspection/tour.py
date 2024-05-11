import math
import subprocess
from dataclasses import dataclass
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from typing import Any, cast, Protocol


answer: int = 42

lines: list[str] = []

fruits: dict[str, int] = {
    "banana": 3,
    "apple": 2,
    "orange": 1,
}

pair: tuple[str, int] = ("banana", 3)

coordinates: tuple[float, float, float] = (4.5, 0.1, 3.2)

numbers: tuple[int, ...] = (1, 2, 3, 4, 5)


class Parrot:
    pass


class NorwegianBlue(Parrot):
    pass


parrot: Parrot = NorwegianBlue()

user_id: int | str = "nobody"  # or 65534

readme = Path("README.md")
description: str | None = None

if readme.exists():
    description = readme.read_text()

if description is not None:
    for line in description.splitlines():
        print(f"    {line}")

assert isinstance(description, str)
for line in description.splitlines():
    ...

description_str = cast(str, description)
for line in description_str.splitlines():
    ...

number1: object = 2
print(number1 + number1)  # error: Unsupported left operand type for +

number2: Any = NorwegianBlue()
print(number2 + number2)  # valid, but crashes at runtime!


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> None:
    print(f"Hello, {name}")


def run(*args: str, check: bool = True, **kwargs: Any) -> None:
    subprocess.run(args, check=check, **kwargs)


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


class Article:
    pass


Serve = Callable[[Article], str]


class Swallow:
    def __init__(self, velocity: float) -> None:
        self.velocity = velocity


@dataclass
class LadenSwallow:
    velocity: float


@dataclass
class Point:
    x: float
    y: float

    def distance(self, other: "Point") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)


type UserID = int | str
type JSON = None | bool | int | float | str | list[JSON] | dict[str, JSON]


def first_str(values: list[str]) -> str:
    for value in values:
        return value
    raise ValueError("empty list")


def first[T](values: Iterable[T]) -> T:
    for value in values:
        return value
    raise ValueError("no values")


fruit: str = first(["banana", "orange", "apple"])
number: int = first({1, 2, 3})


class Joinable(Protocol):
    def join(self) -> None: ...


def join_all(joinables: Iterable[Joinable]) -> None:
    for task in joinables:
        task.join()
