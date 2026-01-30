---
id: SHAPE_NOT_INVARIANTS
title: "Interchange types describe shape, not invariants."
summary: "Interchange types say \"what fields exist\" not \"what values are valid.\" Use primitive types (`str`, `int`, `dict[str, object]`) rather than refined types (`Literal[\"active\"]`, `PositiveInt`, domain-..."
---

Interchange types say "what fields exist" not "what values are valid." Use primitive types (`str`, `int`, `dict[str, object]`) rather than refined types (`Literal["active"]`, `PositiveInt`, domain-specific TypedDicts).

```python
# Good: describes shape, translator validates
class UserPayload(TypedDict):
    status: str  # Translator checks if valid status

# Bad: encodes domain invariants in interchange type
class UserPayload(TypedDict):
    status: Literal["active", "suspended"]  # Domain knowledge leaked
```

**For polymorphic data** (discriminated unions, variable structure), use loose types like `dict[str, object]`. The translator handles discrimination based on fields like `type`.

```python
# Good: translator discriminates and parses
class MessageDict(TypedDict):
    role: str
    content: str | list[dict[str, object]]  # Translator handles content blocks

# Bad: duplicates domain type structure at interchange layer
ContentDict = TextContentDict | ToolUseContentDict | ToolResultContentDict
```

**Why**: Interchange types mirror external formats (JSON), which have no notion of refined types or discriminated unions. Encoding invariants creates duplication between interchange and domain layers, and couples them unnecessarily.