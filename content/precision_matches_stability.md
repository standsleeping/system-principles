---
id: PRECISION_MATCHES_STABILITY
title: "Match type precision to stability."
essence: "Loose types at volatile boundaries, precise types in stable cores; tighten or loosen as understanding solidifies."
---

Types exist on a precision spectrum—from `Any` to refined types like `EmailAddress`. Precision should match stability:

- **Loose types** belong near volatility: external boundaries we can't control, or rapidly-changing areas where locking down prematurely would cause rework.
- **Precise types** belong in stable domains where invariants matter and understanding has solidified.

Track where your types fall on this spectrum. If a loose type has drifted into the domain core, tighten it. If a precise type sits at a volatile boundary, you may be over-specifying.