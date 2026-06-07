---
name: concept-purpose
description: Write and validate a concept's purpose statement against four quality criteria (specific, distinguishing, measurable, concept-focused) rated on 1-5 scales.
---

# Concept Purpose

Write a purpose statement for a concept and evaluate it against four criteria.

## When to use

- After identifying a concept (Stage 1), to define what it's for
- When reviewing an existing concept that feels vague or unmotivated
- When a concept seems purposeless — it may be an exposed mechanism rather than a true concept (p. 65)

## Process

1. Write a one-sentence purpose statement expressing what the concept is *for*.
2. Purposes are not user goals. A goal is what the user wants to achieve; a purpose is what the concept provides (p. 219).
3. Rate the purpose on each of the four criteria (1–5 scale).
4. If any criterion scores below 3, revise the statement and re-rate.

## Criteria

- **Specific (1–5):** How relevant to this concept's design? (1 = vague, 5 = precise)
- **Distinguishing (1–5):** How clearly does it separate this concept from others? (1 = generic, 5 = unique)
- **Measurable (1–5):** How well does it provide a yardstick to evaluate the design? (1 = unfalsifiable, 5 = clear test)
- **Concept-focused (1–5):** How much is it about the concept vs. a broader user goal? (1 = goal-like, 5 = concept-specific)

## Artifact

```
Purpose {
  statement:       str
  specific:        1..5
  distinguishing:  1..5
  measurable:      1..5
  concept_focused: 1..5
}
```

## Persistence

Persist on approval: add `purpose` to the accreting draft `concepts/<name>.json` (created at Stage 1). See the `concept-design` skill's **Persistence protocol**.

## Validation

- A concept without a compelling purpose may not be a concept at all (p. 57).
- If the purpose sounds like it describes a mechanism ("expose the buffer to the user"), the concept is likely an exposed mechanism that should be redesigned (p. 65).
