---
id: STRENGTHEN_OUTPUTS
title: "Provide more by strengthening outputs."
essence: "Provide more by tightening postconditions. Then update the callers that can now rely on the stronger output."
---

"Providing more" means:

1. Strengthening postconditions.
2. Returning more information.
3. Providing richer data structures.
4. Adding guarantees.

If providing more, ask:

1. What data structure(s) capture the "more" we are providing?
2. What functions depend on the new data structure?