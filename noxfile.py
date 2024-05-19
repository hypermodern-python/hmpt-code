"""Checks for HMPT example code."""

import sys
from pathlib import Path

import nox


pythons = ["3.12", "3.11", "3.10"]
chapters = [str(chapter) for chapter in Path().glob("chapter02*")]


@nox.session(python=pythons[0])
def lint(session: nox.Session) -> None:
    """Lint with pre-commit."""
    options = ["--all-files", "--show-diff-on-fail"]
    session.install("pre-commit")
    session.run("pre-commit", "run", *options, *session.posargs)


@nox.session(python=pythons)
def mypy(session: nox.Session) -> None:
    """Type-check with mypy."""
    session.install("mypy")
    session.run("mypy", *chapters)
    if session.python == pythons[0]:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")
