# UI Tooling

Tools and techniques for verifying UI constraints, debugging layout issues, and maintaining visual consistency.

## [UT1] Automatic Verification

Layout constraints should be automatically verified, not manually inspected. When a constraint like "no page-level scrolling" exists, tooling should:

1. Detect violations immediately
2. Identify the specific cause
3. Integrate with automated tests
4. Be available during development

Treat layout bugs as first-class defects with proper tooling support.

## [UT2] Overflow Detection

The core constraint (no page-level scrolling) requires tooling to detect when the document size exceeds the viewport.

### What to Measure

```javascript
// Viewport: what the user sees
const viewport = {
  width: window.innerWidth,
  height: window.innerHeight
};

// Document: how big the page actually is
const document = {
  width: Math.max(body.scrollWidth, html.scrollWidth),
  height: Math.max(body.scrollHeight, html.scrollHeight)
};

// Violation: document larger than viewport
const hasScroll = {
  horizontal: document.width > viewport.width,
  vertical: document.height > viewport.height
};
```

### Per-Element Analysis

For each element, check:

1. Does its bounding rect extend beyond the viewport?
2. Does it have internal scroll (scrollWidth > clientWidth)?
3. What are its computed overflow properties?

This identifies both the symptom (page scrolls) and the cause (specific element).

## [UT3] Ancestry Tracing

When an element causes overflow, trace up the DOM to find where the problem originates:

```
body: 1200x900 (r:1200, b:900)
  main: 1200x900 (r:1200, b:900)
    section: 1200x850 (r:1200, b:850)
      div: 1250x400 (r:1250, b:400) [!RIGHT]  ← overflow starts here
```

The trace shows dimensions and flags where overflow begins, making it clear which ancestor to fix.

## [UT4] Visual Debugging

During development, highlight problematic elements:

1. Red outline on elements causing overflow
2. Data attributes showing the issue type
3. Console report with structured information
4. Watch mode for detecting changes during resize

Visual feedback makes overflow immediately apparent without requiring DevTools inspection.

## [UT5] Test Integration

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

### Structured Reports

Return structured data for programmatic use:

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

## [UT6] Development Workflow

### Browser Console

Load debugging tools on every page during development:

```javascript
UIDebug.scan()           // Find and highlight overflow
UIDebug.traceOverflow(el) // Walk up DOM to find source
UIDebug.measure(el)      // Inspect specific element
UIDebug.watch()          // Monitor during resize
UIDebug.clear()          // Remove highlights
```

### CI/CD Integration

Run layout constraint tests as part of the build:

```bash
# In CI pipeline
uv run pytest tests/system/ -k "scroll"
```

Fail the build if layout constraints are violated.

## [UT7] Diagnostic Output

When constraints are violated, provide actionable diagnostics:

```
[FAIL] Page scrolls (vertical: +47px)
Viewport: 1920x1080
Document: 1920x1127

Overflowing elements (3):
  main.content:
    - Extends 47px past bottom edge
  div#sidebar:
    - Content 23px taller than container
  section.hero:
    - Extends 12px past right edge
```

Include:

1. The violation type and amount
2. Viewport vs document comparison
3. List of contributing elements
4. Specific issue for each element

## [UT8] Continuous Monitoring

For dynamic content or resize behavior, watch for changes:

```javascript
// Check every second, report when state changes
UIDebug.watch(1000);
```

This catches overflow that only appears at certain viewport sizes or after dynamic content loads.

## [UT9] Presenting Results to Users

When reporting debug results (whether to a human developer or in documentation), raw numbers alone are hard to interpret. Effective presentation requires:

1. **Show the math**: Make it obvious how values combine
2. **Visualize spatial relationships**: ASCII diagrams show how elements stack
3. **Highlight the constraint**: Show what should match and whether it does

### Summarizing Measurements

Present key measurements in a table showing the flex/layout relationship:

```
Viewport: 1280 x 720
Document: 1280 x 720  ← Matches exactly, no scroll

Element                  | top    | bottom | height | flex
-------------------------|--------|--------|--------|------------
nav                      | 0      | 61     | 61     | 0 1 auto
main                     | 61     | 720    | 659    | 1 1 0%
.lean-page-container     | 61     | 720    | 659    | 1 1 0%

Math check: 61 + 659 = 720 ✓
```

The "Math check" line makes the constraint explicit and verifiable at a glance.

### ASCII Layout Diagrams

For complex layouts, show how elements nest and where boundaries fall:

```
┌─────────────────────────────────────────┐ top=0
│  nav (flex: 0 1 auto)                   │
│  height: 61px (content-driven)          │
├─────────────────────────────────────────┤ top=61
│  main (flex: 1 1 0%)                    │
│  height: 659px (takes remaining space)  │
│  ┌───────────────────────────────────┐  │
│  │ .content-container (flex: 1)      │  │
│  │ ┌─────────────────────────────┐   │  │
│  │ │ .editor (flex: 1)           │   │  │
│  │ │ height: 471px               │   │  │
│  │ ├─────────────────────────────┤   │  │
│  │ │ .footer                     │   │  │
│  │ │ height: 188px               │   │  │
│  │ └─────────────────────────────┘   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘ bottom=720
```

This visualization shows:

- Nesting relationships (what contains what)
- Boundary positions (where each element starts/ends)
- Flex behavior (which elements are fixed vs flexible)
- How the math adds up to fill the viewport exactly

### Before/After Comparisons

When debugging a fix, show the contrast:

```
BEFORE (broken):
  nav: 53px
  main: calc(100vh - 50px) = 670px  ← Hardcoded assumption
  Total: 53 + 670 = 723px
  Overflow: 723 - 720 = 3px ✗

AFTER (fixed):
  nav: 53px (content-driven)
  main: flex: 1 = 667px (automatic)
  Total: 53 + 667 = 720px ✓
```

This makes the root cause and solution immediately clear.

### Key Insight Callouts

After presenting data, state the key insight explicitly:

> The key insight: `nav` is now 61px (different from before), but it doesn't matter.
> `main` with `flex: 1` automatically takes `720 - 61 = 659px`. No hardcoded values needed.

This connects the raw measurements to the underlying principle being demonstrated.
