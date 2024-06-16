from pathlib import Path

import nox

nox.options.error_on_external_run = True


@nox.session
def build(session):
    session.install("twine")
    session.run("poetry", "build", external=True)
    session.run("twine", "check", *Path().glob("dist/*"))


@nox.session
def tests(session):
    session.install(".", "pytest", "pytest-httpserver", "factory-boy")
    session.run("pytest")
