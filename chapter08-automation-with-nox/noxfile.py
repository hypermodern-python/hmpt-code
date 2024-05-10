import nox


@nox.session
def tests(session):
    session.install("-r", "dev-requirements.txt")
    session.install(".", "--no-deps")
    session.run("pytest")
