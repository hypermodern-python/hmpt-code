import io
import subprocess
import sys

import pytest

from random_wikipedia_article import Article, show


def test_output():
    args = [sys.executable, "-m", "random_wikipedia_article"]
    process = subprocess.run(args, capture_output=True, check=True)
    assert process.stdout


@pytest.fixture
def file():
    return io.StringIO()


articles = [
    Article(),
    Article("test"),
    Article("Lorem Ipsum", "Lorem ipsum dolor sit amet."),
    Article(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        "Nulla mattis volutpat sapien, at dapibus ipsum accumsan eu.",
    ),
]


@pytest.mark.parametrize("article", articles)
def test_final_newline(article, file):
    show(article, file)
    assert file.getvalue().endswith("\n")
