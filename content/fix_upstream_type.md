---
id: FIX_UPSTREAM_TYPE
title: "Fix the upstream type."
summary: "If you need to cast, it means the upstream type is wrong or too loose. Fix the source definition."
---

If you need to cast, it means the upstream type is wrong or too loose. Fix the source definition.

```python
# Bad: casting because upstream returns Any
def get_user_id() -> Any:
    return db.query("SELECT id FROM users")

user_id: UUID = cast(UUID, get_user_id())  # Cast hides the problem

# Good: fix the source
def get_user_id() -> UUID:
    row = db.query("SELECT id FROM users")
    return UUID(row["id"])  # Parse at the boundary

user_id = get_user_id()  # No cast needed
```

When you see a cast, trace it upstream. The fix belongs at the source, not the call site.