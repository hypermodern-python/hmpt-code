import json
import sys
import textwrap
import urllib.request
from dataclasses import dataclass
from typing import Final, TextIO

API_URL: Final = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Article:
    title: str = ""
    summary: str = ""


def fetch(url: str) -> Article:
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    return Article(data["title"], data["extract"])


def show(article: Article, file: TextIO) -> None:
    summary = textwrap.fill(article.summary)
    file.write(f"{article.title}\n\n{summary}\n")


def main() -> None:
    article = fetch(API_URL)
    show(article, sys.stdout)
