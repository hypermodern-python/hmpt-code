import textwrap

import httpx


API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
USER_AGENT = "random-wikipedia-article/0.1 (Contact: you@example.com)"


def main():
    headers = {"User-Agent": USER_AGENT}

    with httpx.Client(headers=headers) as client:
        response = client.get(API_URL, follow_redirects=True)
        response.raise_for_status()
        data = response.json()

    print(data["title"], end="\n\n")
    print(textwrap.fill(data["extract"]))
