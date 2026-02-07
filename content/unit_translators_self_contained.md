---
id: UNIT_TRANSLATORS_SELF_CONTAINED
title: "Unit translators are self-contained."
essence: "The atoms of conversion: each unit translator does one parse with no dependencies and no delegation."
---

A unit translator converts data using only built-in functions. No external dependencies, no calling other translators.

```python
# Unit translator: self-contained conversion
def parse_timestamp(value: str) -> tuple[TranslatorError | None, datetime | None]:
    try:
        return None, datetime.fromisoformat(value)
    except ValueError as e:
        return TranslatorError(f"Invalid timestamp: {e}"), None

# Unit translator: simple type transformation
def parse_uuid(value: str) -> tuple[TranslatorError | None, uuid.UUID | None]:
    try:
        return None, uuid.UUID(value)
    except ValueError:
        return TranslatorError(f"Invalid UUID: {value}"), None
```