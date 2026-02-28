---
id: ISOLATE_SHARED_STATE
title: "Isolate shared state by default."
essence: "Don't share state unless concurrent modification is harmless."
---

For any state shared between actors (threads, processes, services, users), ask: "what if someone modifies this concurrently?" Share state only when concurrent modification is harmless. Sharing requires justification; isolation is the default.

```python
# Shared mutable state: any actor can corrupt another's work
class SharedCart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)  # What if two actors call this concurrently?

cart = SharedCart()
# Actor A and Actor B both modify cart.items — race condition

# Isolated state with explicit exchange: each actor owns its data
def add_item(items: tuple, item: str) -> tuple:
    return items + (item,)

cart_a = add_item((), "book")    # Actor A's cart
cart_b = add_item((), "pencil")  # Actor B's cart
# No sharing, no races — merge only when explicitly needed
```

This principle sits between `STATE_ENTANGLES_TIME` (which observes that state couples values to time) and `STATELESS_DESIGN` (which eliminates state entirely). Not every system can go fully stateless; when state is necessary, isolation is the next best thing. Isolated state preserves the key property of `DEPEND_ON_VALUES`: actors exchange data rather than reaching into each other's internals.
