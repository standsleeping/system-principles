---
id: INTEGRATORS
title: "Integrators."
essence: "Assemble a complex structure or data type. They \"glue together\" different behaviors and produce composite data structures. Characteristics:"
---

Assemble a complex structure or data type. They "glue together" different behaviors and produce composite data structures. Characteristics:

- Calls other units and/or integrators.
- Sole purpose is to assemble complex return types and data structures.
- Delegates to other unit/integrator calls.
- Never makes semantically meaningful decisions: always delegates to other integrators/units.
- Can use if/else but ONLY to conditionally (i.e. early) return its return type.
- Simple integration tests: one test function/suite-of-functions for each `return`.
- Size of test suite is proportional to variety of return conditions.
- Tests NEVER mock or stub user code; always RUNS code that integrator depends on.