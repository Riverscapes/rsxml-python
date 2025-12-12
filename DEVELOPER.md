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

## Release Process

1. **Update Changelog**:
   - Move the content from `[Unreleased]` to a new section with the version number and date in [CHANGELIST.md](CHANGELIST.md).
   - Ensure `[Unreleased]` is empty but preserved at the top.

2. **Bump Version**:
   - Update the version number in [src/rsxml/__version__.py](src/rsxml/__version__.py).

3. **Tag and Push**:
   - Commit the changes (changelog and version bump).
   - Create a git tag matching the version (e.g., `v2.2.0`) NOTE THE "v" it is important that the tag start with this.
   - Push the commit and the tag to GitHub:
     ```bash
     git commit -am "Bump version to 2.2.0"
     git tag v2.2.0
     git push && git push --tags
     ```
   - The [Publish to PyPI](.github/workflows/pypi-publish.yml) GitHub Action will automatically build and deploy the package.
