---
id: REFINED_TYPES_PROPAGATE_PROOFS
title: "Refined types propagate proofs."
essence: "Validate once at the boundary, then trust the type. The type *is* the proof."
---

Once validated, the type carries the proof forward. Functions accepting refined types don't need defensive checks.

Examples: `NonEmptyList[T]`, `VerifiedJwt`, `ParsedEmail`, `PositiveInt`.

Validate once at the boundary, then trust the type. A function that takes `PositiveInt` doesn't check for negative values. A function that takes `ParsedEmail` doesn't re-validate the format. The type *is* the proof.