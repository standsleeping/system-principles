---
id: DATA_DRIVEN_DISPATCH
title: "Prefer data-driven dispatch for evolving domain logic."
essence: "Dictionary-based dispatch separates decisions from behavior, making operations inspectable, testable, and independently evolvable."
---

Pattern matching complects structure (what states exist) with behavior (what to do), making both harder to change independently.

```python
# Pattern matching complects structure and behavior
match user.status:
    case UserStatus.ACTIVE:
        handle_active(user)
    case UserStatus.SUSPENDED:
        handle_suspended(user)

# Data-driven dispatch separates them
handlers = {
    UserStatus.ACTIVE: handle_active,
    UserStatus.SUSPENDED: handle_suspended,
}
result = handlers[user.status](user)
```

The dispatch table separates decisions from handlers, making operations easier to add and test independently.

When you have multiple operations over the same set of variants, dispatch tables scale better:

```python
to_label = {
    UserStatus.ACTIVE: "Active",
    UserStatus.SUSPENDED: "Suspended",
}

to_color = {
    UserStatus.ACTIVE: "green",
    UserStatus.SUSPENDED: "gray",
}
```

You can add to_label, to_color, to_permissions maps independently without touching the enum or other maps.

Dispatch tables are data—inspectable, serializable, composable, and testable:

```python
# Inspect for documentation or metrics
exposed = {k.name: v.__name__ for k, v in handlers.items()}

# Serialize configuration (e.g., to review diffs)
config = {k.value: v.__name__ for k, v in handlers.items()}
```

Use when:

1. Domain logic has changing interpretations
2. Multiple operations exist over the same data
3. Runtime configuration or inspectable decisions are needed

Trade-offs:

1. Adding new variants requires updating each relevant map.
2. No static checker to ensure coverage; manage exhaustiveness explicitly.
