---
id: PARSE_INTO_STRONGER_TYPES
title: "Parse into stronger types."
essence: "Validators should look like parsers: return proof-carrying values, not booleans."
---

Validation returns booleans; parsing returns stronger types that carry the proof forward.

- Translators SHOULD build context-free proofs: presence/shape, normalization, simple formats (UUID, ISO date, email syntax), and cross-field form invariants that require no I/O (e.g., password == confirm).
- Translators MUST NOT implement policy/stateful checks: uniqueness, invites, quotas/rate limits, time-based rules, or config-driven policies (e.g., password strength).
- Prefer strengthening inputs over weakening outputs: construct proof-carrying values (e.g., `EmailAddress`, `ConfirmedPassword`) and return a typed `...Input` object on success.
- Validators should look like parsers: return proof-carrying values, not booleans.