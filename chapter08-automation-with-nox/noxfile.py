import shutil
from pathlib import Path

import nox


@nox.session
def build(session):
    session.install("build", "twine")

    distdir = Path("dist")
    if distdir.exists():
        shutil.rmtree(distdir)

    session.run("python", "-m", "build")
    session.run("twine", "check", *distdir.glob("*"))


@nox.session
def tests(session):
    session.install("-r", "dev-requirements.txt")
    session.install(".", "--no-deps")
    session.run("pytest")
