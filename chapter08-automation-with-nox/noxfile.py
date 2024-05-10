"""
Run the checks and tasks for this project.
"""

import shutil
from pathlib import Path

import nox

nox.options.error_on_external_run = True
nox.options.sessions = ["tests"]


@nox.session
def build(session):
    """Build the package."""
    session.install("build", "twine")

    distdir = Path("dist")
    if distdir.exists():
        shutil.rmtree(distdir)

    session.run("python", "-m", "build")
    session.run("twine", "check", *distdir.glob("*"))


@nox.session(python=["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"])
def tests(session):
    """Run the test suite."""
    session.install(".[tests]")
    try:
        session.run("coverage", "run", "-m", "pytest", *session.posargs)
    finally:
        session.notify("coverage")


@nox.session
def coverage(session):
    session.install("coverage[toml]")
    if any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", "report")
