---
name: spec-definition
description: Complete a SpecDefinition for a concept that was demoted at Stage 9 (Coherence). Handles the demotion path only; bottom-up spec discovery is out of scope (see concept-design).
---

# Spec Definition

Complete a `SpecDefinition` for a concept that was demoted to a Spec at Stage 9. One Spec per file.

This skill is the demotion-completion stage of the concept-design chain. Bottom-up spec discovery is out of scope; see `concept-design`'s "Concepts vs Specs" section.

## When to use

- After Stage 9 (Coherence) emits a `Demotion` reclassifying a candidate concept as a Spec
- When formalizing the result of that demotion as a SpecDefinition

## Process

1. Gather the demoted concept's `ConceptSeed` and the `Demotion` from Stage 9.
2. Construct the `SpecSeed`: copy `name` and `description` from the ConceptSeed; set `kind: "spec"`; set `source: "existing"` (the spec is being recovered from an existing concept candidate).
3. Write the `description`: one paragraph naming the contract or data shape and why it exists.
4. Write the `shape`: the type or structural definition. Use whichever notation is clearest (record syntax, BNF, recursive enum, table of patterns).
5. List `referenced_by`: every Concept whose state or actions reference this Spec, with a one-phrase reason. The Stages 4–5 outputs of the demoted concept's neighbors are the source.
6. Write `semantics`: labeling conventions, role of each field, intended use, and rules of interpretation that aren't obvious from the shape alone.
7. List `invariants`: properties the Spec promises to maintain (totality, uniqueness, stability across edits, etc.).

## Artifact

```
SpecDefinition {
  seed:          SpecSeed
  description:   str
  shape:         str             // type definition in any notation that's clearest
  referenced_by: SpecReference[]
  semantics:     str
  invariants:    str[]
}

SpecReference {
  concept: str                   // a Concept name from the project's concept set
  via:     str                   // which state component or action references this Spec
}
```

Top-level keys are snake_case (`referenced_by`). The seed wraps identification metadata (`kind: "spec"`, `name`, `description`, `source`); top-level identification fields are not allowed.

## Persistence

Persist on approval: write each `SpecDefinition` to `concepts/specs/<name>.json`. The originating demotion (Stage 9) should also have removed the obsolete `concepts/<name>.json`. See the `concept-design` skill's **Persistence protocol**.

## Validation

- The originating `Demotion` must list at least two distinct entries in `signals` (schema-enforced). If the demotion is weakly motivated, revisit it before assembling the spec.
- Every name in `referenced_by.concept` must match a Concept in the project's concept set; cross-check at Stage 13.
- Every Concept named in `referenced_by` should have a state component or action that actually references this Spec (verified at Stage 13).
- A SpecDefinition should have at least two entries in `referenced_by` (Spec test #1). One reference suggests internal helper, not Spec — revert the demotion.
- If the `shape` field is a single-line type with no explanation, the Spec is too thin; either expand `semantics` or revert the demotion.
- Specs do not have `actions`, `state`, `purpose`, or `operational_principle` fields. If you find yourself needing one, the demotion was wrong — revert.
