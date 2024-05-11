import json
import sys
import textwrap
import urllib.request
from dataclasses import dataclass
from typing import Final, TextIO, TypeAlias

API_URL: Final = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Article:
    title: str = ""
    summary: str = ""


JSON: TypeAlias = None | bool | int | float | str | list["JSON"] | dict[str, "JSON"]


def fetch(url: str) -> Article:
    with urllib.request.urlopen(url) as response:
        data: JSON = json.load(response)

    match data:
        case {"title": str(title), "extract": str(extract)}:
            return Article(title, extract)

    raise ValueError("invalid response")


def show(article: Article, file: TextIO) -> None:
    summary = textwrap.fill(article.summary)
    file.write(f"{article.title}\n\n{summary}\n")


def main() -> None:
    article = fetch(API_URL)
    show(article, sys.stdout)
