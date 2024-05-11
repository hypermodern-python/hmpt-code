import sys
import json
import textwrap
import urllib.request
from dataclasses import dataclass

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Article:
    title: str = ""
    summary: str | None = None


def fetch(url):
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    return Article(data["title"], data["extract"])


def show(article: Article, file):
    if article.summary is not None:
        summary = textwrap.fill(article.summary)
    else:
        summary = "[CENSORED]"
    file.write(f"{article.title}\n\n{summary}\n")


def main():
    article = fetch(API_URL)
    show(article, sys.stdout)
