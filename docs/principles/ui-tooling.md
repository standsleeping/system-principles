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

## [UT10] Headless Console Debugging

Use Playwright to programmatically check for JavaScript errors without opening a browser. This catches broken imports, runtime exceptions, and failed network requests that silently break UI functionality.

### The Problem

JavaScript module loading fails silently from the user's perspective. A single broken import can prevent an entire application from initializing, leaving the UI empty with no visible error. Manual browser inspection is slow and easy to forget.

### The Technique

Run a headless browser that captures console errors and failed requests:

```python
from playwright.sync_api import sync_playwright

def check_page_for_errors(url: str) -> dict:
    """Check a page for JS errors and failed requests."""
    errors = []
    failed_requests = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Capture console errors
        page.on('console', lambda msg:
            errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err:
            errors.append(f'Page error: {err}'))

        # Capture failed network requests
        page.on('requestfailed', lambda req:
            failed_requests.append(f'{req.url} - {req.failure}'))

        page.goto(url, timeout=5000)
        page.wait_for_timeout(1000)  # Allow JS to execute

        browser.close()

    return {
        'errors': errors,
        'failed_requests': failed_requests,
        'has_issues': bool(errors or failed_requests)
    }
```

### Inspecting Application State

Check whether the application initialized correctly by querying exposed globals:

```python
# After page.goto() and wait
registry_len = page.evaluate('window.registry?.length ?? "not found"')
app_state = page.evaluate('window.appInstance?.state ?? null')
```

This verifies not just that the page loaded, but that the JavaScript application bootstrapped successfully.

### Common Issues This Catches

1. **Missing files**: Import statements referencing deleted/moved files
2. **Syntax errors**: JS parsing failures that prevent module execution
3. **Network failures**: API endpoints returning 404/500
4. **Initialization errors**: Exceptions thrown during app bootstrap

### Integration with Existing Tests

Add to existing Playwright test fixtures:

```python
@pytest.fixture
def page_without_errors(page: Page):
    """Page fixture that fails on console errors."""
    errors = []
    page.on('console', lambda msg:
        errors.append(msg.text) if msg.type == 'error' else None)
    yield page
    assert not errors, f"Console errors: {errors}"
```

### When to Use

- After refactoring that touches imports or file structure
- When UI appears empty or broken with no visible error
- As a quick sanity check before deeper debugging
- In CI to catch import/initialization regressions

## [UT11] Component Preview Systems

Isolate components for development and testing outside their full application context. A component preview system allows:

1. Viewing components with controlled props
2. Testing responsive behavior at specific widths
3. Comparing variants side-by-side
4. Iterating on styles without full app reload

### Component Contract

Components in the preview system export a standard interface:

```javascript
// Required exports
export const metadata = {
  name: 'ComponentName',
  description: 'What it does',
  category: 'navigation',  // grouping
  source: 'app-name'       // which app owns it
};

export const propTypes = {
  label: { type: 'string', default: 'Click me' },
  disabled: { type: 'boolean', default: false },
  onClick: { type: 'function', default: null }
};

export const variants = [
  { name: 'default', props: { label: 'Click me' } },
  { name: 'disabled', props: { label: 'Disabled', disabled: true } }
];

export function render(props) {
  // Returns DOM element
}

// Optional
export const styles = `
  .component { ... }
`;
```

This contract enables:
- **Registry discovery** - Components self-describe
- **Props editing** - Types define editable controls
- **Variant switching** - Pre-configured states for testing
- **Style injection** - Styles load only when needed

### What Qualifies as a Component

Components in this system are **isolated, stateless render functions**:

| Qualifies | Why |
|-----------|-----|
| Row items, cards, badges | Pure render, simple props |
| Form inputs, buttons | Controlled via props |
| Section headers, labels | No external dependencies |

| Does Not Qualify | Why |
|------------------|-----|
| Stateful classes | Requires lifecycle management |
| Renderers with imports | Has external dependencies |
| Functions taking DOM elements | Props aren't simple values |

The key: can you preview it with just `component.render({ ...props })`?

## [UT12] Width-Controlled Responsive Testing

Test responsive behavior by controlling container width, not viewport width:

```javascript
// In preview system
const preview = document.createElement('div');
preview.style.width = `${this.previewWidth}px`;
preview.appendChild(component.render(props));
```

### Why Container Width, Not Viewport

1. **Faster iteration** - No window resizing
2. **Precise control** - Exact pixel values
3. **Side-by-side comparison** - Same viewport, different widths
4. **Component-level testing** - Tests the component, not the layout

### Width Control UI

Provide slider + input + auto button:

```
[====o========] [280] [Auto]
```

- Slider for quick exploration (120-600px range)
- Input for precise values
- Auto resets to natural container width

### Systematic Breakpoint Analysis

Test components at key widths to understand wrapping behavior:

```
150px: 2 lines (wraps after 2nd item)
200px: 2 lines (wraps after 3rd item)
280px: 1 line (all items fit)
```

Document where natural breakpoints occur, then decide if CSS should enforce them.

## [UT13] Variant-Based Testing

Variants are pre-configured prop sets that represent meaningful states:

```javascript
export const variants = [
  {
    name: 'empty',
    description: 'No data loaded',
    props: { items: [], loading: false }
  },
  {
    name: 'loading',
    description: 'Data loading',
    props: { items: [], loading: true }
  },
  {
    name: 'populated',
    description: 'With sample data',
    props: { items: sampleItems, loading: false }
  }
];
```

### Variant Selection Workflow

1. Click variant to load its props into live preview
2. Width control applies to loaded variant
3. Props inspector updates to show variant's values
4. "default" variant always available to reset

### Designing Variants

Include variants for:

- **Default state** - Baseline/empty props
- **Populated states** - With realistic sample data
- **Edge cases** - Long text, empty data, error states
- **Visual states** - Selected, hover, disabled
- **Responsive stress tests** - Maximum content that might wrap

Variants serve as both documentation and test cases.

## [UT14] Responsive Design Strategy

When building responsive components:

### 1. Start with Natural Flow

Use `flex-wrap: wrap` and let content flow naturally:

```css
.summary {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}
```

### 2. Measure Natural Breakpoints

Use width control to find where content wraps:

| Content Type | Typical Wrap Point |
|--------------|-------------------|
| 3 short metrics | ~200px |
| Type signature + metrics | ~260px |
| Long labels | ~320px |

### 3. Decide: Natural vs Controlled

**Natural wrapping** (flex-wrap):
- Simpler CSS
- Adapts to any content length
- Less predictable visual rhythm

**Controlled breakpoints** (container queries):
- Explicit layout changes
- Predictable visual states
- More CSS complexity

### 4. Test with Variants

Create variants that stress-test wrapping:

```javascript
{
  name: 'long-content',
  props: {
    signature: '(VeryLongTypeName, AnotherLongType) → ReturnType',
    callsCount: 99,
    decisionsCount: 99
  }
}
```

### 5. Document Decisions

Record breakpoint decisions in component or docs:

```javascript
// Responsive behavior:
// < 200px: metrics stack vertically
// 200-280px: metrics wrap to 2 lines
// > 280px: single line
```
