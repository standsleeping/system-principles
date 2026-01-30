---
id: INCLUDE_TEMPORAL_INFO
title: "Include temporal information."
summary: "State-centric models lose temporal information. Track **when** facts became true."
---

State-centric models lose temporal information. Track **when** facts became true.

```python
class User:
    status: UserStatus
    status_changed_at: datetime  # When did this become true?
```

See Events (EV1) for event sourcing and Entity-Attribute-Value-Time models.