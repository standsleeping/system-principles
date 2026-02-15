---
name: concept-actions
description: Enumerate a concept's actions — the operations a user or system can perform that change or query the concept's state.
---

# Concept Actions

Enumerate the actions for a concept.

## When to use

- After formulating the operational principle (Stage 3)
- When detailing a concept's interface before designing its state

## Process

1. List every operation a user or system can perform on this concept.
2. Each action should have a clear name and a brief description of what it does.
3. Actions should be derivable from the operational principle — they are the steps that make the OP's narrative possible.
4. If you can't list actions, the concept may not be a real concept (p. 57).

## Artifact

```
Action {
  name:        str
  description: str
}
```

Produced as a list: `Action[]`

## Validation

- Do the actions cover everything needed to enact the operational principle?
- Is each action user-facing? Internal implementation steps are not actions.
- Are action names clear enough that a user would recognize them?
