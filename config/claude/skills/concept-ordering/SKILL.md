---
name: concept-ordering
description: Derive the order in which a newcomer should pick up a system's concepts — a topological introduction sequence over the dependency graph, so no concept is introduced before the ones it assumes.
---

# Concept Ordering

Produce a **learning path**: the order in which the concepts (and any demoted
specs) should be introduced to someone ramping up, so that reading or being
taught one concept never assumes a concept they have not met yet.

This is the **"no forward references" rule applied at the concept level**. The
writing guidance bans referencing a term before it is defined; this stage bans
*introducing a concept before its prerequisites*. It is the global, ordered
counterpart to `concept-independence` (which tests, pairwise, whether a single
concept can stand alone) and a reading view of `dependency-mapping`'s graph.

## When to use

- After `dependency-mapping` (Stage 8), once the concept set has **settled** —
  i.e. after Stage 9 demotions and Stage 10 genericity collapses. Re-runnable:
  re-run whenever the concept set or its dependencies change.
- When writing documentation, a tutorial, an onboarding path, or a glossary and
  you need a defensible order to introduce the vocabulary.
- When a concept's explanation keeps reaching for not-yet-introduced concepts —
  the order is wrong, or the concept is entangled (send it back to
  `concept-independence`).

## Vocabulary

| Term | Meaning |
|---|---|
| **Primitive** | A foundational concept: a root of the dependency DAG (in-degree zero). Depends on nothing; learned first. |
| **Atomic / freestanding** | A concept understandable without reference to any other (Polanyi/Jackson concept independence). Primitives are always freestanding; later concepts are freestanding *given* their tier's predecessors. |
| **Learning path** | A topological ordering of the dependency DAG grouped into tiers — the introduction sequence. |
| **Tier** | A rank in the ordering. Tier *n* may assume only concepts in tiers `< n`. |
| **Forward reference** | A concept whose introduction needs a concept introduced later. The thing this stage exists to eliminate. |

## Process

1. **Inputs.** Take the `DependencyGraph` from `dependency-mapping` and the
   settled concept set (post-demotion, post-genericity). Demoted specs are
   nodes too: a concept that references a spec assumes that spec.
2. **Find the primitives.** Compute in-degree over the dependency edges. Nodes
   with in-degree zero are the primitives — tier 0. If there are none, there is
   a cycle (see step 5).
3. **Topologically sort into tiers.** Each concept enters the lowest tier that
   sits strictly above all the concepts it depends on. Concepts that depend on
   nothing new beyond a shared tier may share a tier.
4. **Annotate each concept** with `assumes` (its direct prerequisites, all of
   which must fall in earlier tiers) and a one-line `rationale`: the single new
   idea this concept adds on top of what the reader already has.
5. **Validate.**
   - *No forward references:* every `assumes` entry resolves to an earlier tier.
   - *Cycles:* report any. A cycle means the set cannot be taught linearly;
     surface it as a merge/redesign signal (the same finding
     `dependency-mapping` flags as a circular dependency).
6. **Break ties deliberately.** When the DAG admits several valid orders, prefer
   (a) the concept with fewer prerequisites, then (b) the concept that unlocks
   the most downstream concepts (highest out-degree — teach the load-bearing one
   sooner). Record the tie-break used; do not leave the order arbitrary.

## Artifact

```
ConceptOrder {
  concept:   str
  assumes:   str[]    // direct prerequisites; every entry must be in an earlier tier
  rationale: str      // the one new idea this concept adds atop its prerequisites
}

Tier {
  level:    int
  concepts: ConceptOrder[]
}

LearningPath {
  primitives: str[]   // the DAG roots (in-degree 0): the first things learned
  tiers:      Tier[]  // ordered; tier n assumes only concepts in tiers < n
  no_forward_references: bool
  cycles:     str[]   // concept names in any cycle found; empty when acyclic
  tie_breaks: str     // notes on how ambiguous orderings were resolved
}
```

## Persistence

The `LearningPath` is a first-class concept artifact. On approval, persist it to `concepts/learning-path.json` (this stage is the writer; Stage 13 only organizes and checks it). It validates against `learning-path.schema.json` (Level 1) and against four cross-artifact rules at Level 2 (covers all concepts, assumes resolve, no forward references, primitives are roots), run by `/concept-validation` (Stage 14). Include the `$schema` field so the validator auto-discovers it. It is optional: a project that skips ordering simply has no `learning-path.json`, and the validator reports the check as skipped. See the `concept-design` skill's **Persistence protocol** for the chain-wide lifecycle.

## Validation

- Does every concept's `assumes` resolve to a strictly earlier tier? If not, the
  ordering is invalid — fix the tiers or question the dependency.
- Could a newcomer read the concepts top to bottom and never hit a term for a
  concept not yet introduced?
- Are the primitives genuinely freestanding (cross-check against
  `concept-independence`)? A "primitive" that can only be explained by reference
  to a later concept is mis-placed or is really a specialization.
- Is any cycle reported routed back to `dependency-mapping` / `concept-independence`
  for merge-or-split, rather than papered over with an arbitrary cut?

## Relationship to neighboring skills

- **`dependency-mapping`** supplies the graph this stage orders. Ordering adds no
  new edges; it ranks the existing ones.
- **`concept-independence`** tests one pair for atomicity; this stage consumes
  that judgment across the whole set. Independent concepts may share a tier;
  a specialization must follow its general concept.
- **`surface-planning`** decides how each concept surfaces per channel; the
  learning path decides the *order* a documentation/onboarding channel reveals
  them in.

## Origin

Added to answer a recurring need: when a system has many concepts, a newcomer
should not have to read one concept that silently assumes seven others exist.
The dependency graph already encodes the constraints; this stage turns them into
a prescribed introduction order and proves it has no forward references.
