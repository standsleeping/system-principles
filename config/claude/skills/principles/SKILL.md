---
name: principles
description: Search and display design principles from system-principles
disable-model-invocation: true
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Principles

Look up design principles. Accepts a principle ID, keyword, or taxonomy group name.

## Usage

- `/principles DATA_DRIVEN_DISPATCH` — show full detail for a principle by ID
- `/principles translators` — search for principles matching a keyword
- `/principles --group testing` — list all principles in a taxonomy group

## Steps

1. Parse `$ARGUMENTS` to determine what the user wants.
2. If it looks like a principle ID (UPPER_SNAKE_CASE), run:
   `uv run --directory <system-principles> principles show $ARGUMENTS`
3. If it's a `--group <name>`, run:
   `uv run --directory <system-principles> principles list --group $ARGUMENTS`
4. Otherwise, search for the keyword with Grep across the system-principles `content/` directory.
5. Return the results clearly.

Replace `<system-principles>` with the system-principles repository path from your context.
