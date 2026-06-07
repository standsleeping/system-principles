---
name: operational-principle
description: Formulate a concept's operational principle — the demonstration chaining the concept's actions into the operation that achieves its purpose. How a concept is understood; not a use case.
---

# Operational Principle

Formulate the operational principle for a concept: the small narrative in which the concept's **actions are performed in sequence and the purpose visibly results**. Polanyi's formulation, which reached Daniel Jackson via Michael Jackson — the OP shows how a thing's "characteristic parts — its organs — fulfill their special function in combining to an overall operation which achieves the purpose of the machine." Naming the actions, ordering them, and watching the purpose fall out of the order: that is the whole job of this stage.

## Why the OP, and not the state or the actions

You understand a toaster through its operational principle. Imagine explaining one to Newton (Daniel Jackson, *The Essence of Software*, p. 222). You would *not* begin with the **state** — the dial setting that determines cook time, the on/off of the heating element, the timer counting down to ejection. You would *not* begin with the **actions** — that turning the dial adjusts the cook-time component. Those define the behavior completely and explain it not at all; they are the wiring, not the demonstration. You would say what the toaster is *for* — its **purpose**, toasting bread — and then you would *show* him: two slices in the top, knob halfway, push the lever down. That demonstration is the operational principle, and it is how the concept is conveyed. State and actions come afterward, as the mechanism behind the demonstration — if they come up at all.

So this artifact must stand on its own. A reader who has only the purpose and the OP should understand the concept.

## When to use

- After defining a concept's purpose (Stage 2), and before its state and actions.
- When a concept's design feels unjustified or arbitrary.
- When you need to separate the essential scenario from mere use cases.

## One principle, one or more scenarios

The OP is one *principle*. It may take more than one *scenario* to demonstrate it — as many as it takes to show every organ doing its part. Jackson extends the toaster OP to a second scenario for exactly this reason:

- **Canonical:** put two slices in the top → set the knob halfway, say → push the lever down → (it heats; the timer runs) → the toast ejects, browned. *Actions chained; purpose — toasted bread — results.*
- **Second** (because one organ, *cancel*, has not yet been shown): set the knob too high → push the lever → as it begins to burn, press cancel → the toast ejects early.

If an action of the concept never appears in any scenario, either the OP is incomplete or that action does not belong to this concept.

## How to write it

1. **Anchor on the purpose.** The OP must end with that need met. If it ends anywhere else, it is demonstrating something other than this concept.
2. **List the concept's actions** — a first pass; Stage 4 formalizes them. The OP is partly how you discover them.
3. **Order them into the run the User would actually perform**, with concrete, illustrative specifics — "the knob halfway, *say*"; the actor performing a named thing with named values. The actor is always the generic token **User** (never an invented personal name like "Maya"). Concreteness comes from the actions and the values, not from a personal name. Write "User sets the darkness to 4," not "the user configures the setting" (too vague) and not "Maya sets the darkness to 4" (invented name).
4. **Let the purpose result from the chain**, visibly — the last beat is the need met *as a consequence of* the steps, not an assertion appended to them.
5. **Add scenarios until every characteristic action has appeared**, each fulfilling its function in combination with the others.
6. **Demonstration, not description.** Could the reader act it out? If you have written "after X, the system does Y, so that Z" — a schema with no actor and no specifics — you have described the pattern, not demonstrated the concept. Rewrite it with the User in it, performing concrete actions on concrete values.

## Form

`After [User does action₁], [action₂], … [actionₙ] — [the purpose is met].`

Keep it short; Jackson's toaster OP is two sentences. Minimal is correct. *Schematic* is not — aim for minimal-and-concrete, never minimal-and-abstract. Brevity comes from cutting detail, not from generalizing away the User's concrete actions and values.

## OP vs. use case

A use case is a **user goal** — what someone wants to accomplish — and a system has many, often spanning several concepts; use cases are elicited and enumerated. The OP is **one concept's characteristic functioning** — singular, essential, the operation that makes the concept *be* this concept; it is discovered, and there is one of it. Relying on use cases and user stories in its place gives too incomplete a picture and yields implementations that cannot be extended (p. 224).

## Artifact

```
OperationalPrinciple {
  narrative: str   // one or more scenarios, as prose; wrap as { "narrative": "..." }, not a bare string
}
```

## Revisit after Stages 4–5

Writing the OP names the actions and touches the state informally. Once Stage 4 has pinned down the actions and Stage 5 the state, return and run the coverage check: does every action appear in some scenario? does the OP exercise the state components that matter? If not, extend the OP — or question the stray part. The OP is provisional until assembly (Stage 6).

## Persistence

Persist on approval: add `operational_principle` to the accreting draft `concepts/<name>.json`. The OP stays provisional until Stage 6, so expect to overwrite this field after the Stages 4–5 coverage check. See the `concept-design` skill's **Persistence protocol**.

## Validation

- Does the chain of actions visibly produce the purpose — is the need met *because of* the steps?
- Does every characteristic action appear in some scenario, doing its job in combination with the others?
- Could someone who has never seen the system understand the concept from the narrative alone — and act it out?
- Is it a demonstration (the generic **User** actor, concrete specifics) rather than a schematic restatement of the pattern?
- If you could not write a compelling OP: is this actually a concept? A mechanism, a fragment, or two concepts conflated often cannot be given one (p. 57).
