---
id: GENERATE_INVARIANTS_LINT_VARIATION
title: "Generate Invariants; Lint Variation."
essence: "A value that must be identical across many artifacts belongs to one source the others include or are generated from — not duplicated and guarded by a linter. Lint is for what may legitimately differ; generation is for what must not."
related: [CONSTANTS_ARE_VARIABLES, ASSERT_STRUCTURE_NOT_CONTENT, CONCEPTUAL_INTEGRITY]
---

There are two ways to keep N artifacts consistent. Factor the shared part into a single source — a template, an include, a generated file — so divergence is impossible. Or duplicate it into every artifact and write a linter that fails when the copies drift. The second is a workaround for the absence of the first.

## A lint that enforces sameness is duplication wearing a disguise

A rule of the form "every file must contain this exact block" or "these files must match" is a single source of truth spread across N files plus a checker, instead of living in one file. It has all the costs of duplication — every change touches N places, and a contributor can add an (N+1)th artifact that silently omits the block — and it has bought nothing the lint couldn't have prevented by not existing, had the invariant been factored out.

The tell: you find you cannot "fix it everywhere," because there is no everywhere — only N copies and a linter that notices when they disagree.

## Lint is for variation; generation is for invariance

Lint earns its place when the property is genuinely per-artifact and *may* vary: this page declares a nav, that one does not; this module needs a translator, that one is pure. There you are checking a *contract*, not enforcing *sameness*, and there is no single source to factor to. Reserve linting for those. When the thing must be byte-identical or structurally identical everywhere, generate or include it and delete the rule.

## Corollary: assert the property, not the incantation

A presence-check lint (`grep` for `height: 100%`, for a required attribute string) tests that an author *typed* something, not that the property *holds* on the built or rendered artifact. The author can satisfy it with the string in a comment or on the wrong element. When you do need a check rather than a generator, assert the property on the output — render the page and verify it fills and clips the viewport — rather than grepping for the text that usually produces it (compare ASSERT_STRUCTURE_NOT_CONTENT, the same instinct applied to tests).

## The trade

Generation adds a build step and a layer of indirection; for a duplication across two files that rarely changes, a lint or even manual care is the proportionate response. The principle bites when the invariant is load-bearing and spread across many artifacts — and hardest of all when the invariant you most need to add (a first-paint bootstrap, a shared header) has nowhere to live because the build only ever copied files and linted the result.
