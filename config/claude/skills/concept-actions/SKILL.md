---
name: concept-actions
description: Enumerate a concept's actions — the operations a user or system can perform that change or query the concept's state.
---

# Concept Actions

Enumerate the actions for a concept.

## When to use

- After formulating the operational principle (Stage 3)
- When detailing a concept's interface before designing its state

## Process

1. List every operation a user or system can perform on this concept.
2. For each action, give it a name (verb), a function-style signature, a precondition (`requires`), a postcondition (`effects`), and an optional prose description.
3. Actions should be derivable from the operational principle — they are the steps that make the OP's narrative possible.
4. If you can't list actions, the concept may not be a real concept (p. 57).

## Artifact

```
Action {
  name:         str           // verb; recognizable to users
  signature:    str           // e.g. "spawn(parent: Process, image: Executable) -> Process"
  requires:     str | null    // precondition; null when always valid
  effects:      str           // postcondition: what changes after the action runs
  description?: str           // optional prose when signature/requires/effects are insufficient
  streaming?:   bool          // trait: yields progressive output before a final value
  async?:       bool          // trait: returns a job handle; completion arrives later
  idempotent?:  bool          // trait: re-running with the same inputs is safe
  requires_capability?: str | null  // trait: capability a caller must hold
}
```

Produced as a list: `Action[]`

The four optional **traits** are channel-portable properties: any per-channel projection (Stage 7) reads them to decide how to surface the action (an SSE stream vs a chunked HTTP body vs progressive CLI print; a job handle for webhook/cron channels; an idempotency key over HTTP; a capability gate). They live on the action, not the channel, so every channel sees the same truth. Omit a trait when it does not apply.

## Action vs affordance

An **action** is the canonical, channel-portable operation: one signature, the contract. An **affordance** is how a *particular channel* invokes that action: a button click, a `hover`, a slash command, a CLI flag, an HTTP route, an MCP tool descriptor.

Keep affordances out of the action list. `hover` and `click` are pointer affordances, not actions; the action beneath them is something like `inspect(target)` or `enter(modeKey)`. If a candidate "action" only makes sense in one channel (no analogue in CLI/API/MCP without translation), it is an affordance: demote it to the canonical action it invokes. Affordances are recorded per channel at Stage 7 (`surface-planning`), each referencing the action it projects.

## Synthesizing signatures and preconditions

- Use entity names from the concept's state model so signatures cohere across actions.
- Identify what entities are inputs vs outputs vs modified; use `->` to show the return type.
- A query that yields information should return a value; an action that mutates state may return `void` or the modified entity.
- Preconditions express when the action is callable — existence of a referent, an authority check, a state predicate. Use `null` when the action is always valid.
- Keep `description` for nuance that doesn't fit cleanly into signature/requires/effects.

## Validation

- Do the actions cover everything needed to enact the operational principle?
- Is each action user-facing? Internal implementation steps are not actions.
- Are action names clear enough that a user would recognize them?
