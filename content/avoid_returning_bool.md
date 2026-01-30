---
id: AVOID_RETURNING_BOOL
title: "Avoid returning bool."
summary: "Before writing `foo() -> bool`, ask: what information does the caller need after the check? Usually it's not just \"yes/no\" but the validated result, found value, or error details."
---

Before writing `foo() -> bool`, ask: what information does the caller need after the check? Usually it's not just "yes/no" but the validated result, found value, or error details.

```python
# Enables blindness
def is_valid(x: str) -> bool: ...
def contains(d: dict, k: str) -> bool: ...

# Returns evidence
def validate(x: str) -> ValidInput | None: ...
def lookup(d: dict[K, V], k: K) -> V | None: ...
def try_process(item: Item) -> tuple[Result | None, list[Error]]: ...
```