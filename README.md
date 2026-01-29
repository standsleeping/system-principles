# System Principles

Manage and apply system design principles.

## Features

- Python 3.13+
- Standard src-layout package structure
- CLI interface with entry point
- uv for dependency management and builds
- Type checking with mypy
- Linting and formatting with Ruff
- Testing with pytest

## Installation

```bash
uv sync --all-groups
```

This installs the package in editable mode along with dev dependencies.

## Usage

```bash
# Basic usage
principles

# Or as a module
python -m principles

# With custom log level
principles --log-level DEBUG
```

## Maintenance workflow (uv)

To update dependencies with a newer uv and verify everything still works:

```bash
# Refresh lockfile to latest compatible versions
uv lock --refresh

# Sync environment (include dev dependencies)
uv sync --all-groups --refresh

# Run quality checks
uv run pytest -q
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run ty check src
```

If `uv.lock` changes, commit it:

```bash
git add uv.lock
git commit -m "chore: refresh uv.lock with uv $(uv --version)"
```
