---
id: VALIDATE_AT_BOUNDARIES
title: "Validate at boundaries."
summary: "Push validation to system edges. Don't scatter checks throughout the codebase."
---

Push validation to system edges. Don't scatter checks throughout the codebase.

```python
from typing import NewType

PositiveInt = NewType('PositiveInt', int)

def validate_positive(n: int) -> PositiveInt | None:
    return PositiveInt(n) if n > 0 else None

def divide_by(denominator: PositiveInt) -> float:
    return 100.0 / denominator  # No check needed—type carries proof
```