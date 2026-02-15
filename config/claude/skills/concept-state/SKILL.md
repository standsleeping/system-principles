---
name: concept-state
description: Design a concept's state — the local "micromodel" of data needed to support its actions. Each concept gets an independent state model to be merged later.
---

# Concept State

Design the state that supports a concept's actions. This is the concept's "micromodel" — a local data model designed independently.

## When to use

- After enumerating actions (Stage 4)
- When figuring out what data the concept needs to maintain

## Process

1. For each action, ask: what state must exist for this action to work?
2. Define state components with a name, type, and description.
3. Design the state independently of other concepts — it will be merged later (p. 58).
4. Keep the model minimal: only include state that is required by the actions.

## Artifact

```
StateComponent {
  name:        str
  type:        str
  description: str
}

State {
  components: StateComponent[]
}
```

## Validation

- Does every action have the state it needs?
- Is there state that no action uses? Remove it.
- Is the state independent enough to be merged with other concepts' state later?
