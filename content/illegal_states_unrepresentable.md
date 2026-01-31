---
id: ILLEGAL_STATES_UNREPRESENTABLE
title: "Make illegal states unrepresentable."
summary: "Shrink the representable state space to only valid states. Move Any types and try/except close to boundaries; convert to meaningful types immediately."
---

1. Move "Any" types as close as possible to the dependency you can't control.
2. Transform "Any" into meaningful types as soon as possible.
3. Move try/except as close to the dependency you can't control.
4. Convert errors into result types and design for handling them.
5. Shrink the representable state space down to the set of valid states.
6. Input parsing is not business logic. Keep them distinct!