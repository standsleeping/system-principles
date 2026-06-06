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

## Concepts vs Specs

The framework distinguishes two kinds of design objects:

- **Concept** — a user-facing element with its own purpose, actions, and stateful behavior. The unit of the per-concept stages (1–6).
- **Spec** — a named, documented contract or shared data shape that multiple concepts reference but which has no actions, no dynamic state, and no user-facing surface of its own. Load-bearing infrastructure that fulfills no concept-shaped purpose.

A candidate is a Spec if all five tests pass:

| # | Test |
|---|---|
| 1 | Referenced by at least two concepts. |
| 2 | Carries documented semantics. |
| 3 | Has no actions of its own. |
| 4 | Has no dynamic state. |
| 5 | Has no user-facing surface. |

If a candidate fails any of tests 3, 4, or 5, it has the responsibility of a concept. If it passes 3–5 but fails 1 or 2, it is an internal sub-shape or helper, not a Spec.

Within this chain, a Spec arises only via *demotion* at Stage 9 — when Coherence analysis surfaces consistent evidence (no actions, no dynamic state, unsurfaceable, in a state-reference cycle) that a candidate concept should be reclassified. Demoted concepts produce SpecDefinitions through the `/spec-definition` stage. Composition stages (dependencies, coherence, artifacts, validation) cover concepts and any demoted specs together.

Bottom-up spec design — identifying load-bearing infrastructure (shared data shapes, named contracts, cross-cutting envelopes) that was never a concept candidate — is **out of scope** for this chain. A standalone `spec-design` skill chain is planned; the work item lives on the prinzfiles roadmap.

## Pacing: one stage at a time

This workflow is **strictly stage-by-stage**. After each stage produces its artifact, **stop and surface the result for review**. Do not proceed to the next stage until the user has acknowledged the output (explicitly approving it, requesting revisions, or saying to continue).

This applies even when:
- The user's initial request says "run the full chain end-to-end."
- A stage's output looks straightforward and uncontroversial.
- Multiple concepts are being processed at once (each *stage* still pauses, even if it covers all concepts in a batch).

The reason: concept design is a thinking exercise, not a generation exercise. Compounding decisions across stages without review locks in mistakes that are expensive to undo at stage 10 but cheap to fix at stage 2. The user's review at each stage is part of the design process, not a courtesy interrupt.

When you finish a stage, end your message with the artifact and a short prompt like "Ready to continue to Stage N+1?" or "Want to revise any of these before moving on?" — then wait.

## Workflow

### Part 1: Per-Concept Definition

Run stages 1–6 for each concept:

| Stage | Skill | Produces |
|-------|-------|----------|
| 1 | `/concept-identification` | `ConceptSeed` — name, description, source |
| 2 | `/concept-purpose` | `Purpose` — statement rated on 4 criteria (1–5) |
| 3 | `/operational-principle` | `OperationalPrinciple` — the motivating scenario |
| 4 | `/concept-actions` | `Action[]` — operations the user can perform |
| 5 | `/concept-state` | `State` — the local micromodel of data |
| 6 | `/concept-assembly` | `ConceptDefinition` — all parts composed |

**Artifact visibility.** Stages 1–5 do not persist as standalone files. Stage 6
(`/concept-assembly`) composes the seed, purpose, operational principle, actions,
and state into the single `ConceptDefinition` at `concepts/<name>.json`, and
`concept-definition.schema.json` embeds all five sub-artifacts via `$ref`. So the
presence of a concept's file attests stages 1–6 *as a bundle*; an individual
Part-1 stage leaving no separate artifact is by design, not an omission. (Stage
14 validation is likewise transient by design — a report, not a file.)

### Part 1B: Per-Spec Definition (post-demotion only)

For each concept demoted at Stage 9, run a single combined assembly to convert the demotion into a SpecDefinition:

| Skill | Produces |
|-------|----------|
| `/spec-definition` | `SpecDefinition` — name, description, shape, referenced_by, semantics, invariants |

This part runs only when Stage 9 emits one or more demotions. There is no bottom-up SpecSeed creation in this chain (see `Concepts vs Specs` above).

### Part 2: Surface Planning

Run stage 7 for each concept, once you know the target channels:

| Stage | Skill | Produces |
|-------|-------|----------|
| 7 | `/surface-planning` | `ConceptManifest` — how actions/state surface per channel, gaps |

### Part 3: Concept Composition

Run stages 8–12 across the full set of concepts:

| Stage | Skill | Produces |
|-------|-------|----------|
| 8 | `/dependency-mapping` | `DependencyGraph` — inter-concept dependencies (concepts and specs) |
| 9 | `/coherence-analysis` | `CoherenceAssessment` + `DesignCheck` + optional `Demotion[]` (concept → spec) |
| 10 | `/genericity-review` | `GenericityAssessment` per concept and per spec |
| 11 | `/challenge-testing` | `ChallengeAssessment` — taxonomy resilience against externally sourced scenarios |
| 12 | `/concept-ordering` | `LearningPath` — topological introduction order (primitives, tiers, assumed-prior per concept); proves no forward references |

Stage 12 consumes the dependency graph from Stage 8 and the **settled** concept
set (after Stage 9 demotions and Stage 10 collapses), so it runs last in this
part. It is re-runnable: re-run whenever the set or its dependencies change.

### Part 4: Artifact Organization and Validation

Run after composition (or after implementation) to capture design as data and verify consistency:

| Stage | Skill | Produces |
|-------|-------|----------|
| 13 | `/concept-artifacts` | `concepts/` directory — organized JSON files (concept definitions and spec definitions) |
| 14 | `/concept-validation` | Validation report — schema, cross-artifact, and codebase checks (concepts and specs) |

These stages are re-runnable checkpoints. Run `/concept-validation` any time artifacts or implementation change.

### Part 5: Toward Implementation

| Stage | Skill | Produces |
|-------|-------|----------|
| 15 | `/data-model-integration` | `IntegratedDataModel` — merged micromodels into a global data model (persisted to `concepts/integrated-data-model.json`) |
| 16 | `/concept-implementation` | Code modules — concepts translated to module boundaries |

## Persistence protocol

The chain persists incrementally so a run is pausable, resumable, and buildable in pieces. Disk is canonical; the conversation is the editor.

**Persist on approval.** When a stage's output is approved (the pacing pause above), write its artifact immediately — do not defer writes to Stage 13.

**Per-concept stages (1–6) accrete one file.** Stage 1 writes `concepts/<name>.json` carrying just `seed`, referencing `concept-definition.partial.schema.json` with `draft: true`. Stages 2–5 add `purpose`, `operational_principle`, `actions`, `state` to that same file. Stage 6 (`concept-assembly`) completes it: switch its `$schema` to `concept-definition.schema.json` and drop `draft`. Progress for a concept = which sub-fields its file carries; a non-draft file = done through Stage 6.

**Composition stages (8–15) write their own standalone files** when they run (`dependency-graph.json`, `coherence.json`, `learning-path.json`, `integrated-data-model.json`, `surfaces/<name>.json`, …). Stage 13 (`concept-artifacts`) is therefore an **organizer + completeness/staleness checkpoint**, not the first writer.

**Resume** by reading `concepts/`: drafts show which concepts are mid-definition; absent composition files show which later stages have not run; `concept-validation` Level 3 (upstream-timestamp staleness) shows which existing artifacts an upstream edit left out of date and must be re-run. There is no separate status ledger — the artifacts are the progress.

## How to use this workflow

You don't have to run every stage every time. Common entry points:

- **Greenfield design:** Start at stage 1, work through sequentially.
- **Existing system audit:** Start at stage 1 with `source: "existing"`, then jump to stages 8–12 to assess composition, resilience, and introduction order.
- **Single concept deepening:** Enter at whichever stage the concept is missing (e.g., it has a name but no formal purpose — start at stage 2).
- **Surface audit:** Jump to stage 7 to check whether concepts are properly surfaced to users.
- **Resilience check:** Jump to stage 11 to challenge an existing taxonomy with new scenarios.
- **Onboarding / reading order:** Jump to stage 12 (needs a `DependencyGraph` from stage 8) to derive the order a newcomer should pick up the concepts.
- **Validation checkpoint:** Run stages 13–14 to organize artifacts and verify consistency.

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
                    ┌───────────────┬───────────────┬──────────────┐
                    ▼               ▼               ▼              ▼
             DependencyGraph   Coherence    Genericity      Challenge
                    │       Assessment +         │              │
                    │       Demotion[] (opt)     │              │
                    │           │                │              │
                    │           ▼                │              │
                    │     SpecDefinition         │              │
                    │     (per demotion)         │              │
                    │           │                │              │
                    └───────────┴────────────────┴──────────────┘
                                    │
                             LearningPath
                       (topological intro order)
                                    │
                          Concept Artifacts
                       (concepts/ + specs/)
                                    │
                        Concept Validation
                         (3-level checks)
                                    │
                            IntegratedDataModel
                                    ▼
                             Implementation
```
