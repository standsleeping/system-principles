---
name: concept-identification
description: Identify and name concepts in a system or domain. Decompose existing systems by breaking ERDs into smaller diagrams, or derive new concepts from domain analysis.
---

# Concept Identification

Identify and name the concepts in a system. This is the entry point to concept design.

## When to use

- Starting a new project and defining its vocabulary
- Analyzing an existing system to surface its implicit concepts
- Decomposing a database schema or class structure into distinct pieces of functionality

## Process

1. **For new systems:** Analyze the domain. What are the distinct things a user can do or interact with? Each should map to a concept.
2. **For existing systems:** Take the database schema or class structure, represent it as an entity-relation diagram, and break it into smaller diagrams — overlapping on entities but not relations. Each smaller diagram embodies a concept's state (p. 58).
3. Name each concept. Names should be recognizable to users, not implementation jargon.
4. Write a brief description of what the concept is about.

## Artifact

Produce one `ConceptSeed` per identified concept:

```
ConceptSeed {
  name:        str
  description: str
  source:      "new" | "existing"
}
```

## Validation

- Every concept should be user-facing, not an internal mechanism (p. 65).
- If you can't describe what the concept is *for* in a sentence, it may not be a real concept — revisit in the Purpose stage.
