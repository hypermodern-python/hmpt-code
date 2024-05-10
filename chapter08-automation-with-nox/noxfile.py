"""
Run the checks and tasks for this project.
"""
import shutil
from pathlib import Path

import nox

nox.options.error_on_external_run = True


@nox.session
def build(session):
    """Build the package."""
    session.install("build", "twine")

    distdir = Path("dist")
    if distdir.exists():
        shutil.rmtree(distdir)

    session.run("python", "-m", "build")
    session.run("twine", "check", *distdir.glob("*"))


@nox.session
def tests(session):
    """Run the test suite."""
    session.install("-r", "dev-requirements.txt")
    session.install(".", "--no-deps")
    session.run("pytest")
