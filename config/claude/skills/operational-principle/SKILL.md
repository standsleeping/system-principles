---
name: operational-principle
description: Formulate a concept's operational principle — the motivating scenario showing how behavior fulfills purpose. Not a use case; the essential justification for the design.
---

# Operational Principle

Formulate the operational principle for a concept — the narrative showing how its behavior fulfills its purpose.

## When to use

- After defining a concept's purpose (Stage 2)
- When a concept's design feels unjustified or arbitrary
- When you need to distinguish the essential scenario from mere use cases

## Process

1. Write a narrative scenario in the form: "after [trigger], the system [behavior], so that [purpose fulfilled]."
2. This is *not* a use case or user story. It is the single motivating scenario that justifies the entire design (p. 224).
3. The operational principle should explain the concept to someone who has never seen it — like explaining a toaster by making toast (p. 222).
4. If you cannot write a compelling operational principle, the concept may need to be expanded or reconsidered (p. 57).

## What distinguishes an OP from a use case

- A use case describes *one way* to use the concept. The OP motivates *why the concept is designed the way it is* (p. 224).
- Use cases and user stories risk giving too incomplete a picture, leading to implementations that can't be extended (p. 224).
- The OP captures the essential behavioral insight, not just a sequence of steps.

## Artifact

```
OperationalPrinciple {
  narrative: str
}
```

## Validation

- Does the narrative clearly connect behavior to purpose?
- Could someone unfamiliar with the system understand the concept from this narrative alone?
- Does it justify the design as a whole, not just one usage path?
