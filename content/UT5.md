---
id: UT5
title: "Test Integration."
summary: "Layout constraints should be verified in automated tests:"
---

Layout constraints should be verified in automated tests:

```python
def test_page_does_not_scroll(page: Page):
    page.goto("/some-page")
    assert_no_page_scroll(page)
```

The assertion should:

1. Check if document exceeds viewport
2. Provide detailed diagnostics on failure
3. List overflowing elements with their issues
4. Include viewport and document dimensions

**Structured Reports**: Return structured data for programmatic use:

```python
@dataclass
class OverflowReport:
    viewport: dict[str, int]
    document_size: dict[str, int]
    page_scroll: PageScrollInfo
    overflowing_elements: list[OverflowElement]

    def summary(self) -> str:
        """Human-readable summary"""
```

This allows both human inspection and automated processing.