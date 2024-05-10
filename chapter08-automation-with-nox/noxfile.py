import nox


@nox.session
def tests(session):
    session.install(".", "pytest", "pytest-httpserver", "factory-boy")
    session.run("pytest")
