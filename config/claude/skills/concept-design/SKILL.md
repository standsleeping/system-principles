---
name: concept-design
description: A custom conceptual design framework inspired by Daniel Jackson's methodology. Orchestrates a multi-stage workflow from identification through coherence analysis, producing structured artifacts at each stage.
---

# Concept Design

A guided workflow for designing software concepts, organized around a "design as data" principle: design decisions are captured as structured values so that each stage's output feeds cleanly into the next. Every stage uses a dedicated skill and produces a concrete artifact.

## When to use

- Designing a new system's vocabulary of concepts
- Analyzing an existing system to surface and formalize its implicit concepts
- Reviewing a system's concept design for coherence, gaps, or unnecessary specificity

## Pacing: one stage at a time

This workflow is **strictly stage-by-stage**. After each stage produces its artifact, **stop and surface the result for review**. Do not proceed to the next stage until the user has acknowledged the output (explicitly approving it, requesting revisions, or saying to continue).

This applies even when:
- The user's initial request says "run the full chain end-to-end."
- A stage's output looks straightforward and uncontroversial.
- Multiple concepts are being processed at once (each *stage* still pauses, even if it covers all concepts in a batch).

The reason: concept design is a thinking exercise, not a generation exercise. Compounding decisions across stages without review locks in mistakes that are expensive to undo at stage 10 but cheap to fix at stage 2. The user's review at each stage is part of the design process, not a courtesy interrupt.

When you finish a stage, end your message with the artifact and a short prompt like "Ready to continue to Stage N+1?" or "Want to revise any of these before moving on?" — then wait.

## Workflow

### Part 1: Single-Concept Definition

Run stages 1–6 for each concept:

| Stage | Skill | Produces |
|-------|-------|----------|
| 1 | `/concept-identification` | `ConceptSeed` — name, description, source |
| 2 | `/concept-purpose` | `Purpose` — statement rated on 4 criteria (1–5) |
| 3 | `/operational-principle` | `OperationalPrinciple` — the motivating scenario |
| 4 | `/concept-actions` | `Action[]` — operations the user can perform |
| 5 | `/concept-state` | `State` — the local micromodel of data |
| 6 | `/concept-assembly` | `ConceptDefinition` — all parts composed |

### Part 2: Surface Planning

Run stage 7 for each concept, once you know the target channels:

| Stage | Skill | Produces |
|-------|-------|----------|
| 7 | `/surface-planning` | `ConceptManifest` — how actions/state surface per channel, gaps |

### Part 3: Concept Composition

Run stages 8–10 across the full set of concepts:

| Stage | Skill | Produces |
|-------|-------|----------|
| 8 | `/dependency-mapping` | `DependencyGraph` — inter-concept dependencies |
| 9 | `/coherence-analysis` | `CoherenceAssessment` + `DesignCheck` |
| 10 | `/genericity-review` | `GenericityAssessment` per concept |

### Part 4: Artifact Organization and Validation

Run after composition (or after implementation) to capture design as data and verify consistency:

| Stage | Skill | Produces |
|-------|-------|----------|
| 11 | `/concept-artifacts` | `concepts/` directory — organized JSON files with schemas |
| 12 | `/concept-validation` | Validation report — schema, cross-artifact, and codebase checks |

These stages are re-runnable checkpoints. Run `/concept-validation` any time artifacts or implementation change.

### Part 5: Toward Implementation

| Stage | Skill | Produces |
|-------|-------|----------|
| 13 | `/data-model-integration` | `IntegratedDataModel` — merged micromodels into a global data model |
| 14 | `/concept-implementation` | Code modules — concepts translated to module boundaries |

## How to use this workflow

You don't have to run every stage every time. Common entry points:

- **Greenfield design:** Start at stage 1, work through sequentially.
- **Existing system audit:** Start at stage 1 with `source: "existing"`, then jump to stages 8–10 to assess composition.
- **Single concept deepening:** Enter at whichever stage the concept is missing (e.g., it has a name but no formal purpose — start at stage 2).
- **Surface audit:** Jump to stage 7 to check whether concepts are properly surfaced to users.
- **Validation checkpoint:** Run stages 11–12 to organize artifacts and verify consistency.

## Artifact flow

```
ConceptSeed ──► Purpose ──► OperationalPrinciple ──► Action[] ──► State
     │             │                │                    │          │
     └─────────────┴────────────────┴────────────────────┴──────────┘
                                    │
                            ConceptDefinition
                                    │
                            ConceptManifest
                          (surface planning)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
             DependencyGraph   Coherence    Genericity
                    │           Assessment   Assessment
                    │               │               │
                    └───────────────┴───────────────┘
                                    │
                          Concept Artifacts
                           (JSON + schemas)
                                    │
                        Concept Validation
                         (3-level checks)
                                    │
                            IntegratedDataModel
                                    ▼
                             Implementation
```
