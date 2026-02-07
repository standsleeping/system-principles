---
id: NO_KNOWLEDGE_AS_CONTROL_FLOW
title: "Do not store knowledge as control flow."
essence: "Knowledge stored as data can be inspected and changed; knowledge stored as branching is frozen in code structure."
---

Each `if` encodes an assumption and a decision. Local branching couples code to context. It hardens behavior and raises change cost.

```python
# Bad: knowledge encoded as control flow
def get_discount(user: User) -> float:
    if user.tier == "gold":
        return 0.20
    elif user.tier == "silver":
        return 0.10
    else:
        return 0.0

# Good: knowledge as data
DISCOUNTS = {
    "gold": 0.20,
    "silver": 0.10,
}

def get_discount(user: User) -> float:
    return DISCOUNTS.get(user.tier, 0.0)
```

The data-driven version is inspectable, testable, and changeable without modifying code structure.