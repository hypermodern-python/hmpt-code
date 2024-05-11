import inspect
import sys
from typing import Any, dataclass_transform, TypeVar


T = TypeVar("T")


def build_dataclass_init(cls: type[T]) -> str:
    annotations = inspect.get_annotations(cls)

    args: list[str] = ["self"]
    body: list[str] = []

    for name, type in annotations.items():
        args.append(f"{name}: {type.__name__}")
        body.append(f"    self.{name} = {name}")

    return "def __init__({}) -> None:\n{}".format(
        ", ".join(args),
        "\n".join(body),
    )


@dataclass_transform()
def dataclass(cls: type[T]) -> type[T]:
    sourcecode = build_dataclass_init(cls)

    globals = sys.modules[cls.__module__].__dict__
    locals: dict[str, Any] = {}
    exec(sourcecode, globals, locals)

    cls.__init__ = locals["__init__"]  # type: ignore[method-assign]
    return cls
