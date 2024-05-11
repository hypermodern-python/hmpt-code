import inspect


def build_dataclass_init[T](cls: type[T]) -> str:
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
