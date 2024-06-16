import io
import subprocess
import sys

import pytest
from factory import Factory, Faker

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


class ArticleFactory(Factory):
    class Meta:
        model = Article

    title = Faker("sentence")
    summary = Faker("paragraph")


article = parametrized_fixture(Article("test"), *ArticleFactory.build_batch(10))


def test_final_newline(article, file):
    show(article, file)
    assert file.getvalue().endswith("\n")


def test_trailing_blank_lines(article, file):
    show(article, file)
    assert not file.getvalue().endswith("\n\n")


@pytest.fixture
def serve(httpserver):
    def f(article):
        json = {"title": article.title, "extract": article.summary}
        httpserver.expect_request("/").respond_with_json(json)
        return httpserver.url_for("/")

    return f


def test_fetch(article, serve):
    assert article == fetch(serve(article))
