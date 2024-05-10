import sys
from dataclasses import dataclass
from importlib.metadata import metadata

import httpx
from rich.console import Console

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
USER_AGENT = "{Name}/{Version} (Contact: {Author-email})"


@dataclass
class Article:
    title: str = ""
    summary: str = ""


def fetch(url):
    fields = metadata("random-wikipedia-article")
    headers = {"User-Agent": USER_AGENT.format_map(fields)}

    with httpx.Client(headers=headers, http2=True) as client:
        response = client.get(url, follow_redirects=True)
        response.raise_for_status()
        data = response.json()

    return Article(data["title"], data["extract"])


def show(article, file):
    console = Console(file=file, width=72, highlight=False)
    console.print(article.title, style="bold")
    if article.summary:
        console.print(f"\n{article.summary}")


def main():  # pragma: no cover
    article = fetch(API_URL)
    show(article, sys.stdout)
