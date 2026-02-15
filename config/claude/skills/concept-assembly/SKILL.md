---
name: concept-assembly
description: Assemble a complete concept definition by composing seed, purpose, operational principle, actions, and state into a single ConceptDefinition.
---

# Concept Assembly

Compose the outputs of Stages 1–5 into a complete concept definition.

## When to use

- After completing identification, purpose, operational principle, actions, and state for a concept
- As a checkpoint to verify internal consistency before moving to composition

## Process

1. Gather the artifacts from Stages 1–5: `ConceptSeed`, `Purpose`, `OperationalPrinciple`, `Action[]`, `State`.
2. Assemble them into a single `ConceptDefinition`.
3. Verify consistency:
   - Does the purpose match the operational principle's narrative?
   - Do the actions cover the steps in the operational principle?
   - Does the state support all the actions?
   - Do the purpose criteria scores all meet minimum thresholds?

## Artifact

```
ConceptDefinition {
  seed:                  ConceptSeed
  purpose:               Purpose
  operational_principle: OperationalPrinciple
  actions:               Action[]
  state:                 State
}
```

## Validation

- The definition should be self-contained: someone reading it should understand the concept without external context.
- If inconsistencies surface during assembly, return to the relevant stage and revise.
