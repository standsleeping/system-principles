---
id: ACCEPTABLE_BOOLS
title: "Acceptable bools."
summary: "Pure predicates where no additional context exists: `is_empty(list)`, `is_prime(n)`, `is_even(n)`."
---

Pure predicates where no additional context exists: `is_empty(list)`, `is_prime(n)`, `is_even(n)`.

The test: after calling the function, does the caller need anything besides yes/no? If the answer is "no, just whether it's true," a bool is fine. If the caller might want "which one?" or "why not?" or "the valid version," return that instead.