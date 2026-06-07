---
name: coherence-analysis
description: Assess whether composed concepts form a coherent whole using three criteria (common mission, reformulability, non-conflict) and structural design checks.
---

# Coherence Analysis

Assess whether a set of composed concepts forms a coherent design.

## When to use

- After mapping dependencies (Stage 8)
- When evaluating whether a system's concepts work well together
- When a design feels bloated, redundant, or internally contradictory

## Process

### Coherence criteria (p. 140)

Rate each on a 1–5 scale:

1. **Common mission:** Do the concepts share a higher-level purpose? Identify it.
2. **Reformulable:** How cleanly can the purposes merge into a single statement? (1 = resist unification, 5 = read as one idea)
3. **Non-conflicting:** How little tension exists between parts? (1 = subtly at odds, 5 = fully complementary)

### Structural design checks (p. 165)

For the system as a whole, verify:

- **Specificity:** Concepts and purposes are one-to-one.
- **No redundant concepts:** No two concepts for one purpose.
- **No missing concepts:** No purpose without a concept to fulfill it.
- **No purposeless concepts:** No concept without a purpose.
- **No overloaded concepts:** No concept serving two purposes.
- **Familiarity:** Same purpose across apps uses the same concept.
- **Integrity:** Composition doesn't break any concept's purpose.

### Demotions (concept → spec)

Demotion is a *recovery path* for candidates that were initially identified as Concepts at Stage 1 but turn out to be Specs after working through the per-concept stages. Most Specs in a system are discovered bottom-up at Stage 1 and never appear here; demotions catch the cases where an initial classification was wrong.

When a candidate concept fails the concept tests consistently across stages, coherence analysis may emit a `Demotion`, reclassifying the candidate as a Spec. The four recognized signals are:

| Signal | Stage | What it means |
|---|---|---|
| `stage_4_zero_actions` | 4 (Actions) | Zero user-facing actions; only system-internal queries or author-time declarations. |
| `stage_5_no_dynamic_state` | 5 (State) | No dynamic state of its own; only static configuration plus a relation that mirrors another concept's state. |
| `stage_7_fully_unsurfaced` | 7 (Surface) | Every action is unsurfaced in every channel. |
| `stage_8_state_reference_cycle` | 8 (Dependencies) | A bidirectional state-reference cycle with another concept (the structural signature of a relation modeled as two entities). |

A demotion records the source concept, the resolution (drop entirely, or keep as a named Spec), the supporting `signals` (at least two), and free-form `rationale` for context. Demoted concepts are then assembled via `/spec-definition` instead of `/concept-assembly`, and the concept's purpose, OP, actions, and state stages are discarded.

## Artifact

```
CoherenceAssessment {
  concepts:        str[]
  common_mission:  str
  reformulable:    1..5
  non_conflicting: 1..5
  notes:           str
  demotions:       Demotion[]   // optional; empty if no concept is being reclassified
}

DesignCheck {
  specificity_holds:       bool
  no_redundant_concepts:   bool
  no_missing_concepts:     bool
  no_purposeless_concepts: bool
  no_overloaded_concepts:  bool
  familiarity_holds:       bool
  integrity_holds:         bool
}

Demotion {
  from_concept: str             // name of the concept being demoted
  to:           "spec" | "drop" // becomes a Spec, or removed entirely
  signals:      Signal[]        // at least 2 distinct signals from the table above
  rationale:    str             // free-form context tying the signals to specifics
}

Signal = "stage_4_zero_actions"
       | "stage_5_no_dynamic_state"
       | "stage_7_fully_unsurfaced"
       | "stage_8_state_reference_cycle"
```

## Persistence

Persist on approval: write the `CoherenceAssessment` (with any `Demotion[]`) to `concepts/coherence.json`. When a demotion reclassifies a concept as a spec, run `/spec-definition` and remove the obsolete `concepts/<name>.json`. See the `concept-design` skill's **Persistence protocol**.

## Validation

- If coherence scores are low, consider splitting or merging concepts.
- Each failed design check should produce a specific recommendation for repair.
- Each `Demotion` must list at least two distinct entries in `signals`. The schema enforces this; a single weak signal is insufficient grounds for demotion.
- After emitting demotions, re-run dependency mapping (Stage 8) and coherence analysis (Stage 9) on the post-demotion concept set, verifying that the cycle or redundancy has resolved.
