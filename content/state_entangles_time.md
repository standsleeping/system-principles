---
id: STATE_ENTANGLES_TIME
title: "State entangles values and time."
essence: "With state, you must know *when* to ask; without state, you only need to know *what* to ask."
---

Stateful approaches are squarely at odds with simple designs, because by definition, state entangles values and time.

```python
# Stateful: value depends on when you ask
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

c = Counter()
c.increment()  # 1
c.increment()  # 2  (same call, different answer)

# Stateless: value depends only on inputs
def increment(count: int) -> int:
    return count + 1

increment(0)  # 1
increment(1)  # 2  (different input, predictable output)
```

With state, you must know *when* to ask. Without state, you only need to know *what* to ask.