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

## Artifact

```
CoherenceAssessment {
  concepts:        str[]
  common_mission:  str
  reformulable:    1..5
  non_conflicting: 1..5
  notes:           str
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
```

## Validation

- If coherence scores are low, consider splitting or merging concepts.
- Each failed design check should produce a specific recommendation for repair.
