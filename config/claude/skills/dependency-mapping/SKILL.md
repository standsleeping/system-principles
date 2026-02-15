---
name: dependency-mapping
description: Identify dependencies between concepts — where one concept's state or actions reference another. Produce a dependency graph for the system.
---

# Dependency Mapping

Identify how concepts depend on one another and produce a dependency graph.

## When to use

- After assembling multiple concept definitions (Stage 6+)
- When understanding the structure of a multi-concept system
- When evaluating whether concepts are properly decoupled

## Process

1. For each pair of concepts, ask: does one concept's state or actions reference the other?
2. A dependency means concept A cannot function without concept B (p. 105).
3. Record each dependency with a reason explaining the relationship.
4. Assemble dependencies into a graph.

## Artifact

```
ConceptDependency {
  concept:    str
  depends_on: str
  reason:     str
}

DependencyGraph {
  concepts:     ConceptDefinition[]
  dependencies: ConceptDependency[]
}
```

## Validation

- Are there circular dependencies? These suggest concepts that should be merged or redesigned.
- Are there concepts with no dependencies and no dependents? They may be isolated — verify this is intentional.
- Does the dependency structure match your intuition about the system's architecture?
