---
id: PD5
title: "Decisions as data."
summary: "Represent dispatch choices as values (e.g., dicts, maps). Decisions become inspectable, serializable, composable, and testable... just like data! This aligns with a functional core where data flows..."
---

Represent dispatch choices as values (e.g., dicts, maps). Decisions become inspectable, serializable, composable, and testable... just like data! This aligns with a functional core where data flows through transformations. Prefer configuration and error information as data to keep control declarative and handling composable.

```python
handlers = {
    UserStatus.ACTIVE: handle_active_user,
    UserStatus.SUSPENDED: handle_suspended_user,
}

# Can inspect for documentation or metrics
exposed = {k.name: v.__name__ for k, v in handlers.items()}

# Serialize configuration (e.g., to review diffs)
config = {k.value: v.__name__ for k, v in handlers.items()}
```