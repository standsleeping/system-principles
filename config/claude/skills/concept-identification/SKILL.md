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

This stage produces only `ConceptSeed`s. SpecSeeds do not originate here; they arise only via Stage 9 demotion (when a candidate fails the concept tests after working through Stages 2–8). If you encounter a candidate that obviously looks like a Spec (a shared data shape or named contract referenced by multiple concepts but with no actions, no dynamic state, no user-facing surface), set it aside; bottom-up spec discovery is out of scope here. Do not introduce SpecSeeds at this stage.

## Artifact

Produce one `ConceptSeed` per identified concept:

```
ConceptSeed {
  kind:        "concept"
  name:        str
  description: str
  source:      "new" | "existing"
}
```

## Persistence

This stage is the first writer: on approval, create `concepts/<name>.json` carrying just `seed`, with `draft: true` and `$schema` pointing at `concept-definition.partial.schema.json`. Stages 2–6 accrete the remaining fields into this same file. See the `concept-design` skill's **Persistence protocol** for the full accreting-file lifecycle.

## Validation

- Every concept should be user-facing, not an internal mechanism (p. 65).
- If you can't describe what the concept is *for* in a sentence, it may not be a real concept — revisit in the Purpose stage.
