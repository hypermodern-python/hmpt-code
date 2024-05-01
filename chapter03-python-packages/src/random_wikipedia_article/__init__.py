import json
import textwrap
import urllib.request


def __getattr__(name):
    if name != "__version__":
        msg = f"module {__name__} has no attribute {name}"
        raise AttributeError(msg)

    from importlib.metadata import version

    return version("random-wikipedia-article")


API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


def main():
    with urllib.request.urlopen(API_URL) as response:
        data = json.load(response)

    print(data["title"], end="\n\n")
    print(textwrap.fill(data["extract"]))
