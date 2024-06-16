import subprocess
import sys


from random_wikipedia_article import show


def test_output():
    args = [sys.executable, "-m", "random_wikipedia_article"]
    process = subprocess.run(args, capture_output=True, check=True)
    assert process.stdout


def test_final_newline(article, file):
    show(article, file)
    assert file.getvalue().endswith("\n")
