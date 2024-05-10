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


@nox.session(python=["3.12", "3.11", "3.10"])
def tests(session):
    """Run the test suite."""
    session.install(".", "pytest", "pytest-httpserver", "factory-boy")
    session.run("pytest")
