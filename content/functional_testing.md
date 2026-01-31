---
id: FUNCTIONAL_TESTING
title: "Functional testing patterns."
summary: "Tests focus on input/output pairs for our functional codebase. Single assertion per test where possible. Never patch/mock/stub code."
---

Tests focus on input/output pairs for our functional codebase. Single assertion per test where possible. Never patch/mock/stub code.

```python
def test_parse_email_extracts_domain():
    result = parse_email("user@example.com")
    assert result.domain == "example.com"
```

Input goes in, output comes out, assertion checks it. No setup, no teardown, no mocking. If a test needs mocking, the design needs work.