---
id: MOCKING_INDICATES_PROBLEMS
title: "Mocking indicates design problems."
summary: "If your tests need to patch application code, refactor the design. Extract units (pure functions) and integrators (assemblers) so they are directly testable. Move side effects to explicit boundary ..."
---

If your tests need to patch application code, refactor the design. Extract units (pure functions) and integrators (assemblers) so they are directly testable. Move side effects to explicit boundary adapters invoked by actions. Represent outcomes with result types instead of exceptions to simplify testing.