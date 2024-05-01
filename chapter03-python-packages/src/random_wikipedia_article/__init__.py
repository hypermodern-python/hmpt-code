import json
import textwrap
import urllib.request
from importlib.metadata import version

__version__ = version("random-wikipedia-article")

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


def main():
    with urllib.request.urlopen(API_URL) as response:
        data = json.load(response)

    print(data["title"], end="\n\n")
    print(textwrap.fill(data["extract"]))
