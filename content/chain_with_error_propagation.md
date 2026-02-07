---
id: CHAIN_WITH_ERROR_PROPAGATION
title: "Chain translators with explicit error propagation."
essence: "Chained translators short-circuit on the first error, keeping every failure visible and traceable."
---

When composing translators, propagate errors explicitly. Don't hide failures.

```python
# Chaining translators
class TranslatorChain[T1, T2, T3]:
    def __init__(
        self,
        first: callable[[T1], tuple[TranslatorError | None, T2 | None]],
        second: callable[[T2], tuple[TranslatorError | None, T3 | None]]
    ):
        self.first = first
        self.second = second

    def __call__(self, input_data: T1) -> tuple[TranslatorError | None, T3 | None]:
        err, intermediate = self.first(input_data)
        if err:
            return err, None

        return self.second(intermediate)

# Usage
json_to_domain = TranslatorChain(
    first=parse_json_to_dict,
    second=dict_to_user_command
)
```