from importlib.metadata import metadata

import httpx
from rich.console import Console

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
USER_AGENT = "{Name}/{Version} (Contact: {Author-email})"


def build_user_agent():
    fields = metadata("random-wikipedia-article")
    return USER_AGENT.format_map(fields)


def main() -> int:
    headers = {"User-Agent": build_user_agent()}

    with httpx.Client(headers=headers, http2=True) as client:
        response = client.get(API_URL, follow_redirects=True)
        response.raise_for_status()
        data = response.json()

    console = Console(width=72, highlight=False)
    console.print(data["title"], style="bold", end="\n\n")
    console.print(data["extract"])

    return 0
