---
id: CONSISTENT_ERROR_TYPES
title: "Keep translator error types consistent."
summary: "Use a standard error type across all translators. This makes error handling uniform."
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