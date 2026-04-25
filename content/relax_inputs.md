---
id: RELAX_INPUTS
title: "Require less by relaxing inputs."
essence: "Require less by weakening preconditions. Then pick defaults that cover the cases the weaker contract now permits."
---

"Requiring less" means:

1. Relaxing preconditions.
2. Accepting broader inputs.
3. Requiring fewer inputs.

If requiring less, ask:

1. What data constraints can we remove or make optional?
2. What functions need to be updated to handle the broader input space?
3. What default values or behaviors handle the now-optional cases?