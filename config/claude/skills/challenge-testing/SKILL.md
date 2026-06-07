---
name: challenge-testing
description: Stress-test a concept taxonomy against externally sourced scenarios. Map each scenario onto the existing concepts; classify how well the taxonomy holds; surface missing concepts, overloaded purposes, and awkward compositions.
---

# Challenge Testing

Probe a concept taxonomy with scenarios that were not used during design. Genericity review asks whether each concept could be more general; challenge testing asks whether the *whole set* survives contact with reality.

## When to use

- After genericity review (Stage 10), once individual concepts are stable.
- When the design has been quiet for a while and you want a resilience check before implementation.
- When real user requests, support tickets, or competitor features have surfaced and you want to see whether the existing concepts cover them.
- After adding or removing a concept, to check whether the new set still answers the same scenarios.

## Where scenarios come from

A challenge is only useful if it was not part of the design. Strong sources:

- Real user requests, support tickets, or interview transcripts.
- Edge cases the team flagged but did not design for.
- Adjacent or competing products: how would this taxonomy handle their feature set?
- Future feature ideas that have been discussed but not committed.
- Failure modes from the existing system (if migrating an existing design).

Weak sources: scenarios invented while designing the concepts (these test memory, not resilience). If the only available scenarios are weak, say so in the notes.

## Process

1. Collect scenarios. Aim for 5-15. Each scenario is one short paragraph describing what someone wants to do or what is happening.
2. For each scenario:
   1. Walk through the concept set and identify which concepts and actions would participate.
   2. Classify the outcome (see below).
   3. List the concepts involved.
   4. Describe what specifically happens: which concept stretches, which action is missing, which composition is awkward.
   5. Propose a response: extend an action, split a concept, add a concept, or accept the gap.
3. Rate overall resilience (1-5) assuming the proposed responses are applied.
4. Record any patterns across scenarios: a recurring strain on one concept, a recurring missing capability, a class of scenarios the taxonomy systematically rejects.

## Outcomes

| Outcome | Meaning |
|---------|---------|
| `clean` | Scenario maps onto existing concepts and actions without strain. |
| `strained` | A concept is asked to do something at the edge of its purpose; risks purpose dilution if accepted as-is. |
| `missing` | No concept or action covers the scenario; suggests a new concept, a new action, or that the scenario is out of scope. |
| `awkward` | Coverage exists but requires complex or unnatural coordination across multiple concepts. |

A scenario classified `clean` is evidence the taxonomy holds. A taxonomy with too many `clean` outcomes and no `strained` or `missing` outcomes either has unusually good coverage or unusually weak scenarios; check the source quality.

## Artifact

```
ChallengeAssessment {
  concepts:   str[]               -- concepts being challenged (matches dependency-graph)
  scenarios:  Scenario[]
  resilience: 1..5                -- overall after proposed responses
  notes:      str?                -- patterns, weak sources, follow-up
}

Scenario {
  id:                str          -- stable identifier (e.g. "scenario-001")
  description:       str          -- one paragraph
  source:            str          -- where it came from
  outcome:           enum         -- clean | strained | missing | awkward
  concepts_involved: str[]        -- concepts that participated or would need to
  details:           str          -- what specifically happens
  proposed_response: str          -- extend, split, add, or accept gap
}
```

The artifact lives at `concepts/challenges.json` and validates against `challenge-assessment.schema.json` in the `concept-artifacts` skill.

## Persistence

Persist on approval: write the `ChallengeAssessment` to `concepts/challenges.json` when this stage runs, rather than deferring to Stage 13. See the `concept-design` skill's **Persistence protocol**.

## Validation

- Resilience is not a coverage score. A taxonomy can score 5 with one `missing` scenario if the proposed response is "accept gap" and the gap is genuinely out of scope.
- A `strained` outcome is more dangerous than a `missing` one: missing concepts are visible and can be added; strained concepts silently dilute their purpose over time.
- If multiple scenarios strain the same concept, that concept is probably overloaded. Cross-check against the `no_overloaded_concepts` flag from coherence analysis.
- If multiple scenarios miss in the same shape, a concept is probably absent. Cross-check against `no_missing_concepts`.
- Scenarios classified `awkward` often indicate a missing composition concept or an unstated relation in the dependency graph.
