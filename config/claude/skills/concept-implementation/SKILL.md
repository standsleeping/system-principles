---
name: concept-implementation
description: Translate the integrated data model and concept definitions into code modules. Each concept maps to a module boundary.
---

# Concept Implementation

Translate the integrated model and concept definitions into code modules.

## When to use

- After data model integration (Stage 11)
- When moving from design artifacts to working code
- When establishing module boundaries for a concept-driven system

## Process

1. For each `ConceptDefinition`, create a module boundary.
2. Translate `State` into the module's data structures (classes, types, schemas).
3. Translate `Action` values into function signatures (the module's public interface).
4. Use the `OperationalPrinciple` to guide integration tests: the OP's narrative describes the scenario the test should exercise.
5. Use the `IntegratedDataModel` to resolve shared entities into shared data structures that multiple modules reference.

## Mapping

| Design Artifact | Code Artifact |
|----------------|--------------|
| `ConceptDefinition` | Module boundary |
| `State` | Data structures (classes, types, schemas) |
| `Action[]` | Function signatures (public interface) |
| `OperationalPrinciple` | Integration test scenario |
| `IntegratedDataModel` | Shared data layer |

## Validation

- Does each module's public interface match the concept's `Action[]`?
- Do the data structures faithfully represent the concept's `State`?
- Is there an integration test that exercises the operational principle's narrative?
- Do module boundaries align with concept boundaries (no module spanning multiple concepts, no concept split across modules)?
