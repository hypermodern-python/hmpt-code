import io

import pytest

from random_wikipedia_article import Article

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


@pytest.fixture(params=articles)
def article(request):
    return request.param
