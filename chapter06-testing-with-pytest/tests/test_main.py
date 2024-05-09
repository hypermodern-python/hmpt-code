import io
import subprocess
import sys

import pytest

from random_wikipedia_article import Article, fetch, show


def test_output():
    args = [sys.executable, "-m", "random_wikipedia_article"]
    process = subprocess.run(args, capture_output=True, check=True)
    assert process.stdout


@pytest.fixture
def file():
    return io.StringIO()


def parametrized_fixture(*params):
    return pytest.fixture(params=params)(lambda request: request.param)


article = parametrized_fixture(
    Article(),
    Article("test"),
    Article("Lorem Ipsum", "Lorem ipsum dolor sit amet."),
    Article(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        "Nulla mattis volutpat sapien, at dapibus ipsum accumsan eu.",
    ),
)


def test_final_newline(article, file):
    show(article, file)
    assert file.getvalue().endswith("\n")


@pytest.fixture
def serve(httpserver):
    def f(article):
        json = {"title": article.title, "extract": article.summary}
        httpserver.expect_request("/").respond_with_json(json)
        return httpserver.url_for("/")

    return f


def test_fetch(article, serve):
    assert article == fetch(serve(article))
