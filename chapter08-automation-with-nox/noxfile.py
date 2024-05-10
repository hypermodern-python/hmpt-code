"""
Run the checks and tasks for this project.
"""
from pathlib import Path

import nox
from nox_poetry import session

nox.options.error_on_external_run = True
nox.options.sessions = ["tests"]


@session
def build(session):
    """Build the package."""
    session.install("twine")
    session.run("poetry", "build", external=True)
    session.run("twine", "check", *Path().glob("dist/*"))


def install_coverage_pth(session):
    output = session.run(
        "python",
        "-c",
        "import sysconfig; print(sysconfig.get_path('purelib'))",
        silent=True,
    )
    purelib = Path(output.strip())
    (purelib / "_coverage.pth").write_text(
        "import coverage; coverage.process_startup()"
    )


@session(python=["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"])
def tests(session):
    """Run the test suite."""
    session.install(".", "coverage[toml]", "pytest", "pytest-httpserver", "factory-boy")
    install_coverage_pth(session)

    try:
        args = ["coverage", "run", "-m", "pytest", *session.posargs]
        session.run(*args, env={"COVERAGE_PROCESS_START": "pyproject.toml"})
    finally:
        session.notify("coverage")


@session
def coverage(session):
    """Generate the coverage report."""
    session.install("coverage[toml]")
    if any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", "report")
