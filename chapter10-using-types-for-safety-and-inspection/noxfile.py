"""
Run the checks and tasks for this project.
"""

import platform
import shutil
import sys
from pathlib import Path

import nox

nox.options.error_on_external_run = True
nox.options.sessions = ["lint", "mypy", "tests"]


def constraints(session: nox.Session) -> Path:
    filename = f"python{session.python}-{sys.platform}-{platform.machine()}.txt"
    return Path("constraints") / filename


@nox.session(python=["3.12", "3.11", "3.10"], venv_backend="uv")
def lock(session: nox.Session) -> None:
    """Lock the dependencies."""
    filename = constraints(session)
    filename.parent.mkdir(exist_ok=True)
    session.run(
        "uv",
        "pip",
        "compile",
        "pyproject.toml",
        "--upgrade",
        "--quiet",
        "--all-extras",
        f"--output-file={filename}",
    )


@nox.session
def build(session: nox.Session) -> None:
    """Build the package."""
    session.install("build", "twine")

    distdir = Path("dist")
    if distdir.exists():
        shutil.rmtree(distdir)

    session.run("python", "-m", "build")
    session.run("twine", "check", *distdir.glob("*"))


@nox.session(python="3.12")
def lint(session: nox.Session) -> None:
    """Lint using pre-commit."""
    options = ["--all-files", "--show-diff-on-fail"]
    session.install(f"--constraint={constraints(session)}", "pre-commit")
    session.run("pre-commit", "run", *options, *session.posargs)


@nox.session(python=["3.12", "3.11", "3.10"])
def mypy(session: nox.Session) -> None:
    session.install(f"--constraint={constraints(session)}", ".[typing,tests]")
    session.run("mypy", "src", "tests")
    session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


def install_coverage_pth(session: nox.Session) -> None:
    output = session.run_install(
        "python",
        "-c",
        "import sysconfig; print(sysconfig.get_path('purelib'))",
        silent=True,
    )
    if output is None:
        return  # --no-install

    purelib = Path(output.strip())
    (purelib / "_coverage.pth").write_text(
        "import coverage; coverage.process_startup()"
    )


@nox.session(python=["3.12", "3.11", "3.10"])
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install(f"--constraint={constraints(session)}", ".[tests]")
    install_coverage_pth(session)

    try:
        args = ["coverage", "run", "-m", "pytest", *session.posargs]
        session.run(*args, env={"COVERAGE_PROCESS_START": "pyproject.toml"})
    finally:
        session.notify("coverage")


@nox.session(python="3.12")
def coverage(session: nox.Session) -> None:
    """Generate the coverage report."""
    session.install(f"--constraint={constraints(session)}", "coverage[toml]")
    if any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", "report")
