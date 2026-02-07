---
id: STRUCTURE_REFLECTS_CHANGE
title: "Structure reflects sources of change."
essence: "Module boundaries should reflect distinct sources of change."
---

Per Parnas, we must focus our designs such that the structure of our system reflects the sources of change.

If pricing rules change weekly but transaction logic is stable, your module boundaries should isolate pricing—not group code by technical layer.

```
# Bad: organized by technical layer (changes scatter)
/models/order.py      # pricing + shipping + fulfillment
/views/order.py       # pricing + shipping + fulfillment
/services/order.py    # pricing + shipping + fulfillment

# Good: organized by change source (changes are local)
/pricing/             # all pricing logic (changes often)
/shipping/            # all shipping logic
/fulfillment/         # all fulfillment logic (stable)
```

Ask: "When X changes, how many files do I touch?" Fewer is better.