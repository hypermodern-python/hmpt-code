import json
import sys
import textwrap
import urllib.request
from dataclasses import dataclass
from typing import Final, TextIO, TypeAlias

import cattrs.gen

API_URL: Final = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Article:
    title: str = ""
    summary: str = ""


JSON: TypeAlias = None | bool | int | float | str | list["JSON"] | dict[str, "JSON"]


converter = cattrs.Converter()
converter.register_structure_hook(
    Article,
    cattrs.gen.make_dict_structure_fn(
        Article,
        converter,
        summary=cattrs.gen.override(rename="extract"),
    ),
)


def fetch(url: str) -> Article:
    with urllib.request.urlopen(url) as response:
        data: JSON = json.load(response)
    return converter.structure(data, Article)


def show(article: Article, file: TextIO) -> None:
    summary = textwrap.fill(article.summary)
    file.write(f"{article.title}\n\n{summary}\n")


def main() -> None:
    article = fetch(API_URL)
    show(article, sys.stdout)
