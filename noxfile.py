import nox

# This file defines the automation tasks for the project using Nox.
# Nox is a command-line tool that automates testing in multiple Python environments.
# To run all sessions: uv run nox
# To run a specific session: uv run nox -s lint


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session):
    """
    Run the test suite using pytest.
    This session installs the package in editable mode with dev dependencies
    and runs the tests across the specified Python versions.
    """
    session.install(".[dev]")
    session.run("pytest")


@nox.session
def lint(session):
    """
    Run linting checks using ruff.
    Ruff is a fast Python linter and code formatter.
    """
    session.install("ruff")
    session.run("ruff", "check", ".")
