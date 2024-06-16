import nox


@nox.session
@nox.parametrize(
    ["python", "django"],
    [
        (python, django)
        for python in ["3.12", "3.11", "3.10"]
        for django in ["3.2.*", "4.2.*"]
        if (python, django) not in [("3.12", "3.2.*"), ("3.11", "3.2.*")]
    ],
)
def tests(session, django):
    session.install(".", "pytest-django", f"django=={django}")
    session.run("pytest")
