---
id: SHIFT_VALIDATION_LEFT
title: "Shift validation left."
essence: "Validate at the workflow phase where the data is authored, not at the phase where it is consumed; deferred failures are bugs in the API, not in the input."
related: [CHASE_CHECKS_UPSTREAM, VALIDATE_AT_BOUNDARIES, ILLEGAL_STATES_UNREPRESENTABLE, ENCODE_BY_FAILURE_MODE, HOIST_DECISIONS]
---

A *deferred failure* is one whose root cause is authored at time T₁ and whose surface symptom appears at time T₂, where T₂ may be hours, weeks, or release cycles later. The longer T₂ − T₁, the harder the failure is to diagnose, the further it is from the person who can fix it, and the more catastrophic the user experience: the report finally generates, the certificate finally renders, the export finally runs, and *then* the system blows up.

The fix is not better error messages at T₂. The fix is to move the check to T₁.

## Two timelines to keep straight

`CHASE_CHECKS_UPSTREAM` and `VALIDATE_AT_BOUNDARIES` push checks upstream along the *code path*: from interior logic toward the API boundary, so a single function ingests a refined type instead of an unchecked one. `SHIFT_VALIDATION_LEFT` pushes checks earlier along the *human workflow timeline*: from the moment a record is *used* back to the moment it was *authored*.

The two are complementary. Boundary validation answers "where in the call stack does this get checked?" Left-shifted validation answers "at which step of the user's process does this get checked?" A system can have crisp boundary types and still defer validation for years if the boundary sits downstream of authoring.

## Symptoms

- The same record is touched at multiple workflow phases (configure, review, publish, consume); only the last phase complains.
- An error message names a field the current user did not author and cannot edit from where they are standing.
- Bug reports of the form "X failed, *but only when generated*" or "this used to work."
- The model has many optional fields whose optionality is conditional (required only when a flag is set, only when a sibling record exists, only for certain consumers).

## The move

1. Identify the consumer that fails. Enumerate the fields it actually reads.
2. Walk back to the authoring surface for each field. That surface is now the responsible party.
3. Encode the requirement at the authoring step: as a presence validation, a required form field, a *ready* state that gates progression, or a checklist the author sees.
4. Replace the consumer's nil-deref with a precondition check that returns a structured "not ready, missing X" result rather than a crash.

The result: the failure now surfaces at T₁, addressed to the person who authored the record, naming a field they can edit immediately. T₂ becomes a no-op for the failure case.

## When deferral is correct

Some validations cannot be left-shifted: invariants that depend on data not yet available at authoring time (e.g., a downstream record that hasn't been created), or rules that genuinely change between T₁ and T₂. For those, deferral is the design, not a bug; surface the deferred check as a typed precondition (`ENCODE_BY_FAILURE_MODE`, loud-failure bucket) so the consumer's interface signals the dependency rather than hiding it.

The test for misplaced deferral: *if the consumer's check fails, could the author have known at T₁?* If yes, the check is in the wrong place.
