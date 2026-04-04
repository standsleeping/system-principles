---
id: CONSTANTS_ARE_VARIABLES
title: "One product's constant is a better product's variable."
essence: "Any hardcoded choice is a missed opportunity for configurability; expose decisions as settings."
---

A design that fixes a value where a user might reasonably want a different one is leaving capability on the table. The discipline is to notice when you are making a choice on the user's behalf and ask whether that choice should be theirs instead.

This applies at every layer: visual settings, algorithm parameters, feature toggles, data formats. When adding a new feature, check that every visual or behavioral decision it introduces has a corresponding configuration surface. A value that seems obvious today becomes a constraint tomorrow.

The test: if changing the value requires editing source code, it is a constant that should probably be a variable.
