## Working locally

It's recommended that you use `RSXML-RiverscapesXML.code-workspace` if you're in VSCode. This workspace is designed around our common development environment.

Always work on a branch and use a pull request.

### Prerequisites

- [uv](https://github.com/astral-sh/uv) for dependency management.
- [pre-commit](https://pre-commit.com/) for git hooks.

### Setup

1. Install dependencies:
   ```bash
   uv sync --all-extras --dev
   ```
2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Running tests

We use `nox` to run tests across multiple Python versions.

```bash
nox
```

## Running examples locally

In order to run the examples you will need to install `rsxml`. If you want that installed version to be editable, you can use `pip install -e .` from the root rsxml directory.

## Deploying

There are two scripts to deploy the package to PyPI:

- `build.sh` - builds the package and puts it in `dist/`.
- `deploy.sh` - Push the package to the PyPI server. This script requires `PYPI_TOKEN` environment variable.

The scripts will automatically install `uv` if it is not present.
