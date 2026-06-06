---
name: data-model-integration
description: Merge individual concept micromodels into a global data model. Micromodels overlap on shared entities but not on relations.
---

# Data Model Integration

Merge the individual concept micromodels (each concept's `State`) into a global data model.

## When to use

- After completing concept composition (Stages 8–10)
- When moving from concept design toward implementation
- When you need a unified data model that supports all concepts

## Process

1. Collect all `State` micromodels from the `DependencyGraph` (which contains all `ConceptDefinition` values).
2. Identify shared entities across micromodels. Concepts may overlap on entities (e.g., both a "Reservation" concept and a "Billing" concept reference a "User" entity) but not on relations (p. 58).
3. Merge overlapping entities into a single entity in the global model.
4. Preserve each concept's relations as distinct; do not merge relations from different concepts.
5. Verify that the integrated model still supports every concept's actions.

## Input

`DependencyGraph` (which contains all `ConceptDefinition` values and their `State` micromodels).

## Artifact

```
IntegratedEntity {
  name:        str
  source_concepts: str[]   -- which concepts share this entity
  fields:      StateComponent[]
}

IntegratedDataModel {
  entities:  IntegratedEntity[]
  relations: IntegratedRelation[]
}

IntegratedRelation {
  name:           str
  source_concept: str      -- the concept this relation belongs to
  from_entity:    str
  to_entity:      str
  cardinality:    str
}
```

## Persistence

The `IntegratedDataModel` is a first-class concept artifact. Export it to
`concepts/integrated-data-model.json` with a `$schema` field; it validates
against `integrated-data-model.schema.json` (Level 1) and against two
cross-artifact rules at Level 2 (covers all concepts, sources are known
concepts), run by `/concept-validation`. It is optional: a project that stops
before implementation prep simply has no `integrated-data-model.json`, and the
validator reports the check as skipped.

## Validation

- Does every concept's `State` map cleanly into the integrated model?
- Are shared entities merged, while relations remain concept-specific?
- Can every concept's actions still be supported by the integrated model?
- Are there entity conflicts (same name, incompatible fields) that need resolution?
