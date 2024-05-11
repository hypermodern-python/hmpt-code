from __future__ import annotations

import io
import subprocess
import sys
from collections.abc import Callable
from typing import Any, cast

import pytest
import pytest_httpserver
from factory import Factory, Faker

from random_wikipedia_article import Article, fetch, show


def test_output() -> None:
    args = [sys.executable, "-m", "random_wikipedia_article"]
    process = subprocess.run(args, capture_output=True, check=True)
    assert process.stdout


@pytest.fixture
def file() -> io.StringIO:
    return io.StringIO()


def parametrized_fixture(*params: Any) -> Any:
    return pytest.fixture(params=params)(lambda request: request.param)


class ArticleFactory(Factory):  # type: ignore[type-arg]
    class Meta:
        model = Article

    title: Faker[Any, str] = Faker("sentence")
    summary: Faker[Any, str] = Faker("paragraph")


article = parametrized_fixture(Article("test"), *ArticleFactory.build_batch(10))


def test_final_newline(article: Article, file: io.StringIO) -> None:
    show(article, file)
    assert file.getvalue().endswith("\n")


@pytest.fixture
def serve(httpserver: pytest_httpserver.HTTPServer) -> Callable[[Article], str]:
    def f(article: Article) -> str:
        json = {"title": article.title, "extract": article.summary}
        httpserver.expect_request("/").respond_with_json(json)
        return cast(str, httpserver.url_for("/"))

    return f


def test_fetch(article: Article, serve: Callable[[Article], str]) -> None:
    assert article == fetch(serve(article))
