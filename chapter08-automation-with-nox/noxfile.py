"""
Run the checks and tasks for this project.
"""

import platform
import shutil
import sys
from pathlib import Path

import nox

nox.options.error_on_external_run = True
nox.options.sessions = ["tests"]


def constraints(session):
    filename = f"python{session.python}-{sys.platform}-{platform.machine()}.txt"
    return Path("constraints") / filename


@nox.session(venv_backend="uv")
def lock(session):
    session.run(
        "uv",
        "pip",
        "compile",
        "pyproject.toml",
        "--upgrade",
        "--quiet",
        "--all-extras",
        "--output-file=constraints.txt",
    )


@nox.session
def build(session):
    """Build the package."""
    session.install("build", "twine")

    distdir = Path("dist")
    if distdir.exists():
        shutil.rmtree(distdir)

    session.run("python", "-m", "build")
    session.run("twine", "check", *distdir.glob("*"))


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


@nox.session(python=["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"])
def tests(session):
    """Run the test suite."""
    session.install("-c", "constraints.txt", ".[tests]")
    install_coverage_pth(session)

    try:
        args = ["coverage", "run", "-m", "pytest", *session.posargs]
        session.run(*args, env={"COVERAGE_PROCESS_START": "pyproject.toml"})
    finally:
        session.notify("coverage")


@nox.session
def coverage(session):
    session.install("-c", "constraints.txt", "coverage[toml]")
    if any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", "report")
