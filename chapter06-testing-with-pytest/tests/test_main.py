import http.server
import io
import json
import subprocess
import sys
import threading

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


@pytest.fixture(scope="session")
def httpserver():
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            article = self.server.article
            data = {"title": article.title, "extract": article.summary}
            body = json.dumps(data).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    with http.server.HTTPServer(("localhost", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield server
        server.shutdown()
        thread.join()


@pytest.fixture
def serve(httpserver):
    def f(article):
        httpserver.article = article
        return f"http://localhost:{httpserver.server_port}"

    return f


def test_fetch(article, httpserver):
    def serve(article):
        httpserver.article = article
        return f"http://localhost:{httpserver.server_port}"

    assert article == fetch(serve(article))
