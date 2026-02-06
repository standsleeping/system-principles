---
id: ASSERT_STRUCTURE_NOT_CONTENT
title: "Assert on structure, not content."
summary: "In system tests and view tests, verify the presence of structural markers like URLs and data-testid attributes rather than rendered text. Text is volatile; structure is stable."
---

In system tests and view tests, verify the presence of structural markers like URLs and data-testid attributes rather than rendered text. Text is volatile; structure is stable.

After a click or submit, don't check that the next page contains specific words. Instead, check the URL and the presence of a `data-testid` attribute that proves you arrived at the right place.

```python
def test_login_page_submit(page):
    """Submitting valid credentials navigates to the dashboard."""
    page.click("[data-testid='login-submit']")
    assert "/dashboard" in page.url
    assert page.locator("[data-testid='dashboard-root']").is_visible()
```

The same rule applies to view tests: verify `data-view-testid` attributes rather than checking that a heading says "Welcome" or a paragraph contains specific copy. Content changes break tests for the wrong reasons.
