---
id: PATTERN_MATCH_AT_BOUNDARIES
title: "Use in-place pattern matching only at boundaries or tiny, stable sets."
essence: "Pattern matching belongs at boundaries for parsing and serialization, not inside domain logic where it complects structure and behavior."
---

Pattern matching inside domain logic complects structure and behavior, increasing branching complexity. Keep it to parsing, serialization, or very small, stable cases.

```python
# Acceptable boundary match: parsing HTTP JSON payload to domain enum
match payload.get("status"):
    case "active":
        status = UserStatus.ACTIVE
    case "suspended":
        status = UserStatus.SUSPENDED
    case _:
        return bad_request("invalid status")
```

Use when:

1. Boundary parsing/serialization.
2. Tiny, stable sets; throwaway code; hot paths.
3. Time/clock extraction at boundaries; pass time forward as data.

Avoid:

1. Large matches that encode domain policy in core logic