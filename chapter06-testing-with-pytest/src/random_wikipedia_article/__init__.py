import sys
import json
import urllib.request
from dataclasses import dataclass

from rich.console import Console

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Article:
    title: str = ""
    summary: str = ""


def fetch(url):
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    return Article(data["title"], data["extract"])


def show(article, file):
    console = Console(file=file, width=72, highlight=False)
    console.print(article.title, style="bold", end="\n\n")
    console.print(article.summary)


def main():
    article = fetch(API_URL)
    show(article, sys.stdout)
