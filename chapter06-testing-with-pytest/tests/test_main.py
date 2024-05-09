import io
import subprocess
import sys

from random_wikipedia_article import Article, show


def test_output():
    args = [sys.executable, "-m", "random_wikipedia_article"]
    process = subprocess.run(args, capture_output=True, check=True)
    assert process.stdout


def test_final_newline():
    article = Article("Lorem Ipsum", "Lorem ipsum dolor sit amet.")
    file = io.StringIO()
    show(article, file)
    assert file.getvalue().endswith("\n")
