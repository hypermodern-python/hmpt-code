import nox

nox.options.error_on_external_run = True


@nox.session
def tests(session):
    session.install(".", "pytest", "pytest-httpserver", "factory-boy")
    session.run("pytest")
