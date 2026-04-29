# System Principles

A library of design principles for software engineering, with tooling to compile them into agent configuration.

## What This Is

System Principles is a curated collection of ~118 design principles organized by taxonomy (process, conceptual, modeling, structure, types, constructs, testing, layout, visual design). Each principle has an ID, title, essence, and full explanation.

The project includes a concept design methodology (inspired by Daniel Jackson) implemented as a suite of skills for Claude Code. These skills guide structured workflows: concept identification, purpose definition, state modeling, dependency mapping, and coherence analysis.

## Why You'd Use It

- Load design principles into your AI coding assistant so it reasons about your code in terms of established engineering concepts
- Use the concept design skills to structure your software design process
- Compile subsets of principles into path-matched rules (e.g., Python conventions applied to `**/*.py`)

## Installation

```bash
git clone https://github.com/standsleeping/system-principles.git
cd system-principles
uv sync --all-groups
```

## Usage

### Browse principles

```bash
# List principles in a taxonomy group
principles list --group modeling

# Show a specific principle
principles show DATA_DRIVEN_DISPATCH

# Compile a group to markdown
principles compile --group types --format essences
```

### Export to Claude Code

```bash
principles export
```

This compiles principles into `config/claude/` as fragments (loaded every session) and rules (path-matched by file type).

### Build the documentation site

```bash
principles site build
principles site serve
```

### Validate references

```bash
principles validate
```

Lints content, taxonomies, and sets. Reports duplicate IDs, filename/ID mismatches, broken `related:` references, and unknown principle IDs in taxonomy groups or sets. Exits non-zero on any finding.

## Development

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest -q
```
