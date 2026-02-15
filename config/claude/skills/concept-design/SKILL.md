---
name: concept-design
description: A custom conceptual design framework inspired by Daniel Jackson's methodology. Orchestrates a multi-stage workflow from identification through coherence analysis, producing structured artifacts at each stage.
---

# Concept Design

A guided workflow for designing software concepts. Each stage uses a dedicated skill and produces a concrete artifact that feeds into the next stage.

## When to use

- Designing a new system's vocabulary of concepts
- Analyzing an existing system to surface and formalize its implicit concepts
- Reviewing a system's concept design for coherence, gaps, or unnecessary specificity

## Workflow

### Part I: Single-Concept Definition

Run stages 1–6 for each concept:

| Stage | Skill | Produces |
|-------|-------|----------|
| 1 | `/concept-identification` | `ConceptSeed` — name, description, source |
| 2 | `/concept-purpose` | `Purpose` — statement rated on 4 criteria (1–5) |
| 3 | `/operational-principle` | `OperationalPrinciple` — the motivating scenario |
| 4 | `/concept-actions` | `Action[]` — operations the user can perform |
| 5 | `/concept-state` | `State` — the local micromodel of data |
| 6 | `/concept-assembly` | `ConceptDefinition` — all parts composed |

### Part I.5: Surface Planning

Run stage 7 for each concept, once you know the target channels:

| Stage | Skill | Produces |
|-------|-------|----------|
| 7 | `/surface-planning` | `ConceptManifest` — how actions/state surface per channel, gaps |

### Part II: Concept Composition

Run stages 8–10 across the full set of concepts:

| Stage | Skill | Produces |
|-------|-------|----------|
| 8 | `/dependency-mapping` | `DependencyGraph` — inter-concept dependencies |
| 9 | `/coherence-analysis` | `CoherenceAssessment` + `DesignCheck` |
| 10 | `/genericity-review` | `GenericityAssessment` per concept |

### Part III: Toward Implementation

After completing the workflow:

- **Data model integration:** Merge the individual concept micromodels (each concept's `State`) into a global data model. Micromodels overlap on shared entities but not on relations.
- **Implementation:** Each `ConceptDefinition` maps to a module boundary. `State` becomes data structures, `Action` values become function signatures, `OperationalPrinciple` guides integration tests.

## How to use this workflow

You don't have to run every stage every time. Common entry points:

- **Greenfield design:** Start at stage 1, work through sequentially.
- **Existing system audit:** Start at stage 1 with `source: "existing"`, then jump to stages 8–10 to assess composition.
- **Single concept deepening:** Enter at whichever stage the concept is missing (e.g., it has a name but no formal purpose — start at stage 2).
- **Surface audit:** Jump to stage 7 to check whether concepts are properly surfaced to users.
