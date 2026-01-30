---
id: TD3
title: "Strengthen inputs, don't weaken outputs."
summary: ""
---

- Prefer making functions total by strengthening parameter types (e.g., `NonEmptyList[T]`) rather than weakening return types to `| None`.
- Parse into precise types at the boundary or immediately at branch entry when a branch needs stronger invariants.
- Build proofs once and carry them forward in types; avoid repeating boolean checks.