import sys
import json
import textwrap
import urllib.request
from dataclasses import dataclass

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
    summary = textwrap.fill(article.summary)
    file.write(f"{article.title}\n\n{summary}\n")


def main():
    article = fetch(API_URL)
    show(article, sys.stdout)
