import nox


@nox.session
@nox.parametrize("django", ["5.*", "4.*", "3.*"])
def tests(session, django):
    session.install(".", "pytest-django", f"django=={django}")
    session.run("pytest")
