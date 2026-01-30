---
id: ENCODE_PREDICATES
title: "Encode predicates in the model."
summary: "An `if` partitions the state space. **The predicate is a fact derived from an underspecified model**. Encode those facts in the model early, with types, invariants, or simple state machines."
---

An `if` partitions the state space. **The predicate is a fact derived from an underspecified model**. Encode those facts in the model early, with types, invariants, or simple state machines.

Examples of `if` complexity:

1. `if (isValid)` for **data** (invalid states).
2. `if (shouldDoX)` for **behavior** (conditional execution).
3. `if (currentState === X)` for **flow** (sequencing/coordination).
4. `if (format === 'json')` for **transformation** (data reshaping).

Move logic into rules, not code paths, and invalid states will start to disappear.