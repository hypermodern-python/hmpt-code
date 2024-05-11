def format_lines(lines: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    return "\n".join(f"{prefix}{line}" for line in lines)
