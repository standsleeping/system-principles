---
id: TESTABLE_MARKUP
title: "Markup must carry test hooks."
essence: "Test selectors need their own attribute so tests don't couple to class names, text content, or CSS paths. `data-testid` is the explicit contract between markup and tests."
---

Every page includes `data-testid` attributes so that system tests have stable, consistent selectors. Only use `data-testid` to locate elements in tests.

Each HTML template should have at least one `data-testid` attribute on a landmark element. If it doesn't yet, note the nearest relevant element in a comment as a reminder.

This keeps test selectors decoupled from styling (no class names), content (no text matching), and structure (no brittle CSS paths). The test hook is an explicit contract between markup and tests.

For view-level testing, use `data-view-testid` attributes to mark elements that view tests should verify. This separates the concerns of system-level and view-level test hooks.
