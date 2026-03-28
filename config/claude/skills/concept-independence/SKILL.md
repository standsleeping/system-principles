---
name: concept-independence
description: Test whether two concepts are genuinely independent or whether one is a specialization of the other. Fills a gap between concept-purpose (validates one concept) and dependency-mapping (maps state/action references).
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Concept Independence

Test whether two candidate concepts are genuinely independent or whether one collapses into the other.

## When to use

- During concept identification, when two candidates feel suspiciously close
- After writing purpose statements, when "distinguishing" scores are low (3 or below)
- When a concept's purpose seems to require mentioning another concept to make sense
- When two concepts share an implementation mechanism and you aren't sure whether that's coincidence or identity

## The core test

**Can you describe what concept A is *for* without reference to concept B?**

If yes: A and B are independent concepts that may share implementation.
If no: A is likely a specialization, property, or mode of B; not an independent concept.

The test is directional. Check both directions: A without B, and B without A. Three outcomes:

| A without B | B without A | Conclusion |
|-------------|-------------|------------|
| Yes | Yes | Independent concepts |
| Yes | No | B depends on A (B may be a specialization of A) |
| No | Yes | A depends on B (A may be a specialization of B) |
| No | No | Likely the same concept under two names |

## Supplementary checks

### Distinct user intent

Does the designer reach for A and B in response to different needs? "I need to show this entity's active range" (Span) vs. "I need to call attention to this column" (Marker) are different intents even if both use an overlay mechanism.

### Independent state

Could A's state model exist without any reference to B's state? If A's state is a strict subset of B's state plus a scope restriction, A is probably a mode of B.

### Separable actions

Does A have at least one action that B does not, and vice versa? If every action on A is also an action on B (just with a constraint), A is a constrained use of B.

## Artifact

```
IndependenceAssessment {
  concept_a:       str
  concept_b:       str
  a_without_b:     bool      # Can A's purpose be stated without mentioning B?
  b_without_a:     bool      # Can B's purpose be stated without mentioning A?
  distinct_intent: bool      # Does the designer reach for them in response to different needs?
  independent_state: bool    # Can their state models exist independently?
  separable_actions: bool    # Does each have actions the other lacks?
  verdict:         "independent" | "specialization" | "same_concept"
  notes:           str       # Reasoning and any caveats
}
```

## Process

1. Write concept A's purpose without mentioning concept B. Write concept B's purpose without mentioning concept A. Note whether either felt forced or incomplete.
2. Describe the designer intent that leads to reaching for A. Describe the intent for B. Are they different situations?
3. Compare their state models. Is one a subset or restriction of the other?
4. Compare their actions. Are A's actions a subset of B's?
5. Produce the assessment.

## Origin

Discovered during concept identification for a timeline grid system. Overlay, Span, and Marker all shared implementation but served different designer intents. The existing concept skills tested whether a concept was *real* (purpose, actions, OP tests) but not whether two real-seeming concepts were *independent of each other*. Dependency-mapping catches state/action references but not purpose-level entanglement.
