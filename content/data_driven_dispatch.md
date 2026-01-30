---
id: DATA_DRIVEN_DISPATCH
title: "Prefer data-driven dispatch for evolving domain logic."
summary: "When the set of operations grows or changes, dictionary-based (data-driven) dispatch cleanly isolates decisions, enabling straightforward extension and testing."
---

When the set of operations grows or changes, dictionary-based (data-driven) dispatch cleanly isolates decisions, enabling straightforward extension and testing.

```python
# Two operations over UserStatus without touching the enum
to_label = {
    UserStatus.ACTIVE: "Active",
    UserStatus.SUSPENDED: "Suspended",
}

to_color = {
    UserStatus.ACTIVE: "green",
    UserStatus.SUSPENDED: "gray",
}

label = to_label[user.status]
color = to_color[user.status]
```

When you have multiple operations over the same set of variants, dispatch tables scale better. You can add to_label, to_color, to_permissions maps independently without touching the enum or other maps.

Use when:

1. Domain logic has changing interpretations
2. Multiple operations exist over the same data
3. Runtime configuration or inspectable decisions are needed

Trade-offs:

1. Adding new variants requires updating each relevant map.
2. No static checker to ensure coverage; combine with PD7.