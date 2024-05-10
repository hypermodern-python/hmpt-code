"""
Run the checks and tasks for this project.
"""
from pathlib import Path

import nox

nox.options.error_on_external_run = True
nox.options.sessions = ["tests"]


@nox.session
def build(session):
    """Build the package."""
    session.install("twine")
    session.run("poetry", "build", external=True)
    session.run("twine", "check", *Path().glob("dist/*"))


@nox.session(python=["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"])
def tests(session):
    """Run the test suite."""
    session.install(".", "coverage[toml]", "pytest", "pytest-httpserver", "factory-boy")
    session.run("coverage", "run", "-m", "pytest", *session.posargs)


@nox.session
def coverage(session):
    session.install("coverage[toml]")
    if any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", "report")
