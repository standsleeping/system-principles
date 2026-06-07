---
name: genericity-review
description: Review a concept for unnecessary specificity. Look for domain-specific assumptions that could be generalized without losing the concept's purpose.
---

# Genericity Review

Review a concept for respects in which it might fail to be generic.

## When to use

- After coherence analysis (Stage 9)
- When a concept feels too tightly coupled to a specific domain or use case
- As a design exercise to find hidden assumptions (p. 244)

## Process

1. Examine the concept's state, actions, and operational principle.
2. For each, ask: is this specific to the current domain, or could it apply more broadly?
3. List aspects that are unnecessarily specific.
4. Propose adjustments that would achieve greater genericity without losing the concept's purpose.
5. Rate how generic the concept is after proposed adjustments (1–5).

## Artifact

```
GenericityAssessment {
  concept:        str
  specific_to:    str[]
  adjustments:    str[]
  generic_after:  1..5
}
```

## Persistence

Persist on approval: write each `GenericityAssessment` to `concepts/genericity/<name>.json` (specs under `concepts/genericity/specs/<name>.json`). See the `concept-design` skill's **Persistence protocol**.

## Validation

- Genericity is not an end in itself. A concept should be as generic as it can be *without* diluting its purpose.
- If adjustments would weaken the purpose, the specificity may be appropriate.
- Most concepts can be applied in many different contexts on different kinds of data (p. 57).
