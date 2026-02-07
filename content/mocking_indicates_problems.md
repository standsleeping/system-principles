---
id: MOCKING_INDICATES_PROBLEMS
title: "Mocking indicates design problems."
essence: "The need to mock is a signal to extract pure functions and push side effects to boundaries."
---

If your tests need to patch application code, refactor the design. Extract units (pure functions) and integrators (assemblers) so they are directly testable. Move side effects to explicit boundary adapters invoked by actions. Represent outcomes with result types instead of exceptions to simplify testing.