---
id: CONSISTENT_ERROR_TYPES
title: "Keep translator error types consistent."
essence: "A shared error type lets translators compose freely and callers handle errors in one uniform way."
---

Use a standard error type across all translators. This makes error handling uniform.

```python
from dataclasses import dataclass

@dataclass
class TranslatorError:
    """Standard translator error"""
    message: str
    code: str = "TRANSLATION_ERROR"

# All translators use the same error type
type TranslatorFunction[TInput, TOutput] = (
    callable[[TInput], tuple[TranslatorError | None, TOutput | None]]
)
```