# Presenting

These principles govern UI concerns: layout, visual design, and tooling. Good presentation respects viewport constraints and uses systematic verification.

## Layout

Layout principles govern the structural arrangement of UI components: where content lives, what contains what, and how space is allocated.

### [LY1] No Page-Level Scrolling.

No page should ever scroll at the html/body level. Individual components may scroll internally, but the page itself must fit exactly within the viewport. When the document size exceeds the viewport, something is wrong with the CSS layout.

This constraint:

1. Forces intentional scroll containment decisions
2. Prevents accidental overflow from breaking layouts
3. Makes overflow bugs immediately visible
4. Enables predictable, viewport-locked application shells

### [LY2] Viewport-Locked Containers.

The root layout container fills exactly the viewport and prevents page-level scrolling:

```css
.layout {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
```

From this foundation, all scrolling must be explicitly delegated to content regions.

### [LY3] Fixed and Flexible Regions.

Layouts combine fixed-size regions (headers, footers, sidebars) with flexible regions that fill remaining space:

- **Fixed regions**: Use explicit heights/widths via CSS variables (tokens)
- **Flexible regions**: Use `flex: 1` to fill available space
- **Resizable regions**: Constrain with min/max bounds

Example token definitions:

```css
:root {
  --layout-header-height: 48px;
  --layout-sidebar-default-width: 280px;
  --layout-sidebar-min-width: 200px;
  --layout-sidebar-max-width: 500px;
}
```

### [LY4] Scroll Containment.

Scrolling is contained within specific content slots, never at the layout level:

1. Layout containers have `overflow: hidden`
2. Content regions have `overflow-y: auto`
3. Only leaf content areas (sidebars, main content) scroll

This creates a clear hierarchy:

```
layout (overflow: hidden)
├── header (fixed height, no scroll)
├── content (overflow: hidden)
│   ├── sidebar (overflow-y: auto) ← scrolls here
│   └── main (overflow-y: auto)    ← scrolls here
└── footer (fixed height, no scroll)
```

### [LY5] Boundary Ownership.

Components own their own visual boundaries. This applies to both parent/child and sibling relationships.

**Parent/Child: Container Owns Border, Child Owns Padding**

When a container has structural borders (separating header from content, for example), the container defines those borders. Children provide their own internal padding.

This allows "flush" variants where children fill edge-to-edge:

```css
/* Normal: container provides padding */
.sidebar-header {
  padding: var(--spacing-lg) var(--spacing-2xl);
  border-bottom: 1px solid var(--gray-200);
}

/* Flush: child fills to edges, provides its own padding */
.sidebar-header-flush {
  padding: 0;
  border-bottom: 1px solid var(--gray-200);
}
```

**Siblings: Each Component Completes Itself**

When two components sit adjacent, each should be visually complete in isolation. A component shouldn't rely on its neighbor to provide its visual edge.

**Test**: If you render each component alone, which one looks incomplete?

```
nav (no bottom border)     →  looks unfinished
content (no top border)    →  looks fine
```

The nav owns the border because it's incomplete without it:

```css
nav {
  border-bottom: 1px solid var(--gray-200);
}
```

The content area shouldn't add a top border to compensate for the nav's missing boundary. That creates implicit coupling.

### [LY6] Empty State Collapse.

Empty structural elements should automatically hide:

```css
.layout-header:empty,
.layout-footer:empty,
.layout-sidebar-header:empty {
  display: none;
}
```

This allows optional slots to be omitted without leaving empty space.

### [LY7] Layout Variants.

Support multiple layout configurations through modifier classes on a shared base:

| Variant | Description |
|---------|-------------|
| `single-column` | Centered content with max-width |
| `left-sidebar` | Sidebar on left, main content on right |
| `right-sidebar` | Main content on left, sidebar on right |
| `combined` | Both sidebars visible |

The base `.layout` class provides the viewport-locked shell. Variants adjust which regions are visible and how space is distributed.

### Common Overflow Causes

When the no-scroll constraint is violated, common causes include:

1. Using `100vw` for width (includes scrollbar width on some browsers)
2. Mismatched height calculations (e.g., `calc(100vh - 50px)` when nav is not 50px)
3. Flex children with min-height exceeding available space
4. Missing `box-sizing: border-box`
5. Content regions without `overflow: hidden` or `overflow: auto`

### [LY8] Never Calculate What Layout Can Handle.

**Never hardcode a value that depends on another element's size.** This creates duplicated knowledge: one element's size is defined in one place, and a guess about that size is hardcoded elsewhere. When either changes, they drift apart silently.

**The Problem: Duplicated Knowledge**

Consider this common pattern:

```html
<!-- nav.html -->
<nav style="padding: 0.75rem;">...</nav>  <!-- Creates ~53px height -->
```

```css
/* styles.css */
.main-content {
  min-height: calc(100vh - 50px);  /* Assumes nav is 50px */
}
```

The nav's height is implicitly defined by its content and padding (~53px). The main content calculation assumes 50px. This 3px discrepancy causes page scroll, and the bug is invisible until someone notices the layout drifts by a few pixels.

This pattern is fragile because:

- The two values have no connection in code
- Changing nav padding silently breaks the layout
- The "50px" is a magic number with no clear origin
- Debugging requires measuring actual rendered sizes

**The Solution: Let Flexbox Distribute Space**

Instead of calculating remaining space, use flex layout to let the browser handle distribution automatically:

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

nav {
  /* No explicit height; sizes to content */
}

main {
  flex: 1;  /* "Take whatever space remains" */
}
```

Now the nav can be 50px, 53px, or 100px. The main content automatically adjusts. No magic numbers, no synchronization required, no brittleness.

**When You Must Use Explicit Sizes**

If explicit dimensions are truly required (rare), use a single CSS variable that both elements reference:

```css
:root {
  --nav-height: 50px;
}

nav {
  height: var(--nav-height);
}

.main-content {
  min-height: calc(100vh - var(--nav-height));
}
```

This creates a single source of truth. But prefer the flexbox approach: it eliminates the variable entirely.

### [LY9] Beware Common Layout Quirks.

CSS has behaviors that cause unexpected spacing. These don't appear as margin or padding in DevTools, making them hard to diagnose. When debugging mysterious gaps, check for these quirks:

**Inline-Block Baseline Gaps**: Form elements (`textarea`, `input`, `select`) and replaced elements (`img`, `video`) default to `display: inline-block`. Inline-block elements sit on the text baseline, leaving space below for text descenders. Fix: Set `display: block` on form elements in layout contexts, or use `vertical-align: top`. Elements in flex/grid containers are blockified automatically.

**100vw Includes Scrollbar Width**: `width: 100vw` includes the scrollbar width on platforms with visible scrollbars, causing horizontal overflow. Prefer `width: 100%` or flex/grid layouts.

**Margin Collapsing**: Adjacent vertical margins collapse to the larger value. Parent and child margins also collapse if nothing separates them (no padding, border, or content). This causes unexpected spacing and elements "escaping" their containers. Fix: Use padding instead of margin, or use flex/grid (which disables margin collapsing).

## Visual Design

Visual design principles govern aesthetics: how interfaces look, how hierarchy is communicated, and how users perceive structure through typography, color, and spacing.

### [VD1] Typography-Based Hierarchy.

Establish visual importance through typography, not color or decoration:

1. Use font-weight (400, 500, 600, 700) for emphasis levels
2. Use font-size variations (xs, sm, md, lg, xl) for hierarchy
3. Prefer gray-700 for primary content, gray-400 for secondary
4. Avoid colored backgrounds on text elements (badges, labels, inline code)

Typography carries meaning. When weight and size do the work, color becomes available for other purposes (status, interaction, accent).

### [VD2] Transparent by Default.

Small UI elements should not compete for attention:

1. Badges, labels, and inline elements have transparent backgrounds
2. Remove padding and border-radius from small text elements
3. Reserve background colors for major container elements
4. Use white backgrounds for subtle section separation

This reduces visual noise and lets content breathe.

### [VD3] Minimal Borders.

Borders should define structure, not decorate:

1. Use subtle left borders (2px) for visual grouping and hierarchy
2. Use top borders for separating sequential items
3. Avoid rounded corners on small elements (badges, inline code)
4. Use border colors that complement content, not create noise
5. Prefer single-side borders over full boxes

Borders are structural cues. When everything has a border, nothing stands out.

### [VD4] Spacing Strategy.

Use modern CSS layout for spacing:

1. **Flex gap** for spacing between elements (not margins)
2. **Padding** for internal spacing within containers
3. Avoid the margin-bottom anti-pattern
4. Let flex containers manage distribution

```css
/* Prefer this */
.container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

/* Over this */
.container > * {
  margin-bottom: var(--spacing-2);
}
.container > *:last-child {
  margin-bottom: 0;
}
```

Gap-based spacing is more predictable and requires less override logic.

### [VD5] Color Usage.

Reserve color for meaning:

1. Bright accent colors (purple, green) for borders and interactive elements
2. Muted text colors (gray-400) for secondary information
3. Dark text (gray-700) for primary content
4. Avoid using background colors to convey category or meaning

A restrained palette makes intentional color usage more impactful.

### [VD6] Simplification Patterns.

When in doubt, simplify:

| Instead of | Prefer |
|------------|--------|
| Icons | Text (e.g., "true/false" over checkmarks) |
| Uppercase | Lowercase (softer appearance) |
| Background color | Font-weight for emphasis |
| Visual containers | Whitespace for breathing room |
| Decorative borders | Structural borders only |

Each visual element costs attention. Earn that cost.

### [VD7] Focus States.

All interactive elements must have visible focus indicators for accessibility:

1. Use a consistent accent color for all focus states (e.g., purple-500)
2. Two patterns based on element type:

**Bordered elements** (inputs, buttons with borders):
```css
element:focus {
  border-color: var(--purple-500);
  box-shadow: 0 0 0 2px var(--purple-100);
}
```

**Borderless elements** (links, icon buttons):
```css
element:focus {
  outline: 2px solid var(--purple-500);
  outline-offset: 2px;
}
```

Consistency in focus states aids keyboard navigation and accessibility.

### [VD8] Token-Driven Design.

Define design decisions as CSS variables (tokens):

```css
:root {
  /* Typography */
  --font-size-sm: 12px;
  --font-size-base: 13px;
  --font-size-lg: 15px;

  /* Spacing */
  --spacing-sm: 4px;
  --spacing-md: 6px;
  --spacing-lg: 8px;

  /* Colors */
  --color-primary: var(--purple-500);
  --color-text: var(--gray-700);
  --color-text-light: var(--gray-400);
}
```

Benefits:

1. Single source of truth for design decisions
2. Easy global adjustments
3. Semantic naming (--color-primary vs #8300CA)
4. Consistent references across components

### [VD9] Reset-First Approach.

Start from a clean slate:

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

Then build up intentionally. Every margin, every padding should be a deliberate choice, not a browser default.

### [VD10] Responsive Component Design.

Components should present information optimally at every width, never overflowing their container. This requires explicit information hierarchy and graceful degradation.

**Information Hierarchy**: Rank every piece of information by importance:

1. Identity (name, title) - Must always be visible
2. Status (metrics, counts) - Core utility, high priority
3. Detail (types, signatures) - Nice to have, can hide
4. Decoration (icons, badges) - Progressive enhancement

Lower-priority items hide before higher-priority items truncate.

**Width Tiers**: Define explicit layout tiers:

| Tier | Strategy |
|------|----------|
| **Wide** | All information visible, optimal layout |
| **Medium** | Hide lowest-priority items, maintain readability |
| **Narrow** | Abbreviate where possible, hide decorative elements |
| **Minimum** | Essential info only, truncate as last resort |

**Degradation Rules**: Apply in order as width decreases:

1. **Wrap** - Let flex containers wrap naturally
2. **Hide** - Remove low-priority information entirely
3. **Abbreviate** - "3 calls" → "3c", "decisions" → "dec"
4. **Truncate** - Ellipsis on text, only when nothing else works

Never:
- Overflow the container
- Truncate high-priority items while showing low-priority ones
- Create inconsistent line counts across similar items

**Implementation Pattern**:

```css
/* Base: wide layout */
.component__detail { display: block; }
.component__metric { /* full text */ }

/* Medium: hide detail */
@container (max-width: 350px) {
  .component__detail { display: none; }
}

/* Narrow: abbreviate metrics */
@container (max-width: 200px) {
  .component__metric--full { display: none; }
  .component__metric--abbrev { display: inline; }
}
```

Or use JavaScript to select content based on measured width:

```javascript
const width = container.offsetWidth;
const showDetail = width >= 350;
const abbreviate = width < 200;
```

**Consistent Visual Rhythm**: Components at the same tier should have the same line count. Inconsistent heights create visual noise in lists. Design tiers so all items at a given width have predictable dimensions.

**Testing**: Use width-controlled preview (see UT12) to verify no overflow at any width, information degrades in priority order, consistent heights across variants, and readable at minimum supported width.

### [VD11] Data-Ink Ratio and Tabular Alignment.

When presenting repeated metrics across items, optimize for scanability by reducing redundant labels and aligning values vertically.

Edward Tufte's data-ink ratio: maximize information, minimize redundant visual elements. When the same labels repeat on every row, move them to a single header:

```
Instead of:
  Customer       9 fields · 3 consumers · 2 producers
  DeliveryInfo   6 fields · 1 producer

Prefer:
                      F   C   P
  Customer            9   3   2
  DeliveryInfo        6   —   1
```

Guidelines:

1. Deduplicate labels: If a label appears on every row, move it to a header
2. Align numbers vertically: Use CSS grid or fixed-width columns
3. Use tabular numerals: `font-variant-numeric: tabular-nums` for consistent digit widths
4. Use dashes for zeros: `—` is clearer than `0` for "none" or "not applicable"
5. Keep headers minimal: Single letters or short abbreviations with tooltips for full names
6. Right-align numbers: Numbers align on the ones digit for easy comparison

Appropriate when showing 5+ items with the same metric structure where numbers are primary information users need to compare.

**Implementation**:

```css
.metric-grid {
  display: grid;
  grid-template-columns: 1fr repeat(3, 3ch);  /* name + 3 metric columns */
  gap: var(--spacing-xs);
}

.metric-value {
  font-variant-numeric: tabular-nums;
  text-align: right;
}

.metric-empty {
  color: var(--gray-300);
}
```

```html
<!-- Section header with column labels -->
<div class="section-header metric-grid">
  <span>DATA</span>
  <span class="metric-label" title="Fields">F</span>
  <span class="metric-label" title="Consumers">C</span>
  <span class="metric-label" title="Producers">P</span>
</div>

<!-- Data rows -->
<div class="entity-row metric-grid">
  <span>Customer</span>
  <span class="metric-value">9</span>
  <span class="metric-value">3</span>
  <span class="metric-value">2</span>
</div>
```

**Responsive Considerations**: At narrow widths, the tabular layout may need to degrade:

| Width | Strategy |
|-------|----------|
| **Wide** | Full grid with aligned columns |
| **Medium** | Inline format with separators: `9 · 3 · 2` |
| **Narrow** | Abbreviated: `9f 3c 2p` or hide secondary metrics |

The inline format loses alignment benefits but remains compact.

### [VD12] One Signal Per Meaning.

Each piece of information should be communicated once, through one visual channel.

When the same meaning is conveyed through multiple signals, it creates redundancy. The user sees two visual changes but learns one fact. The extra signal is noise.

Choose one visual channel per meaning:

| Meaning | Preferred Signal | Avoid Adding |
|---------|------------------|--------------|
| Navigable/clickable | Text color (blue) | Background color |
| Selected | Background color | Border + background |
| Disabled | Opacity reduction | Gray text + gray background |
| Error state | Text color (red) | Red text + red border + red background |

Multiple signals are appropriate when they serve different purposes: accessibility (focus states may use both outline AND background), different information (blue text for navigable + badge for count convey different facts).

Test for redundancy: "If I remove this visual treatment, does the user lose information?" If no, remove it.

## Tooling

Tools and techniques for verifying UI constraints, debugging layout issues, and maintaining visual consistency.

### [UT1] Automatic Verification.

Layout constraints should be automatically verified, not manually inspected. When a constraint like "no page-level scrolling" exists, tooling should:

1. Detect violations immediately
2. Identify the specific cause
3. Integrate with automated tests
4. Be available during development

Treat layout bugs as first-class defects with proper tooling support.

### [UT2] Overflow Detection.

The core constraint (no page-level scrolling) requires tooling to detect when the document size exceeds the viewport.

**What to Measure**:

```javascript
// Viewport: what the user sees
const viewport = { width: window.innerWidth, height: window.innerHeight };

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

For each element, check: Does its bounding rect extend beyond the viewport? Does it have internal scroll? What are its computed overflow properties? This identifies both the symptom (page scrolls) and the cause (specific element).

### [UT3] Ancestry Tracing.

When an element causes overflow, trace up the DOM to find where the problem originates:

```
body: 1200x900 (r:1200, b:900)
  main: 1200x900 (r:1200, b:900)
    section: 1200x850 (r:1200, b:850)
      div: 1250x400 (r:1250, b:400) [!RIGHT]  ← overflow starts here
```

The trace shows dimensions and flags where overflow begins, making it clear which ancestor to fix.

### [UT4] Visual Debugging.

During development, highlight problematic elements:

1. Red outline on elements causing overflow
2. Data attributes showing the issue type
3. Console report with structured information
4. Watch mode for detecting changes during resize

Visual feedback makes overflow immediately apparent without requiring DevTools inspection.

### [UT5] Test Integration.

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

### [UT6] Development Workflow.

Load debugging tools on every page during development:

```javascript
UIDebug.scan()           // Find and highlight overflow
UIDebug.traceOverflow(el) // Walk up DOM to find source
UIDebug.measure(el)      // Inspect specific element
UIDebug.watch()          // Monitor during resize
UIDebug.clear()          // Remove highlights
```

Run layout constraint tests as part of CI/CD. Fail the build if layout constraints are violated.

### [UT7] Diagnostic Output.

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

Include the violation type and amount, viewport vs document comparison, list of contributing elements, and specific issue for each element.

### [UT8] Continuous Monitoring.

For dynamic content or resize behavior, watch for changes:

```javascript
// Check every second, report when state changes
UIDebug.watch(1000);
```

This catches overflow that only appears at certain viewport sizes or after dynamic content loads.

### [UT9] Presenting Results to Users.

When reporting debug results, raw numbers alone are hard to interpret. Effective presentation requires:

1. **Show the math**: Make it obvious how values combine
2. **Visualize spatial relationships**: ASCII diagrams show how elements stack
3. **Highlight the constraint**: Show what should match and whether it does

Present measurements in tables showing the flex/layout relationship with a "Math check" line that makes the constraint explicit and verifiable at a glance. Use ASCII layout diagrams for complex layouts to show nesting relationships, boundary positions, flex behavior, and how the math adds up. State key insights explicitly after presenting data.

### [UT10] Headless Console Debugging.

Use Playwright to programmatically check for JavaScript errors without opening a browser. This catches broken imports, runtime exceptions, and failed network requests that silently break UI functionality.

JavaScript module loading fails silently from the user's perspective. A single broken import can prevent an entire application from initializing, leaving the UI empty with no visible error.

Run a headless browser that captures console errors and failed requests. Check whether the application initialized correctly by querying exposed globals. Add to existing Playwright test fixtures to fail on console errors.

**Common Issues This Catches**:

1. **Missing files**: Import statements referencing deleted/moved files
2. **Syntax errors**: JS parsing failures that prevent module execution
3. **Network failures**: API endpoints returning 404/500
4. **Initialization errors**: Exceptions thrown during app bootstrap

Use when: after refactoring that touches imports or file structure, when UI appears empty or broken with no visible error, as a quick sanity check before deeper debugging, in CI to catch import/initialization regressions.

### [UT11] Component Preview Systems.

Isolate components for development and testing outside their full application context. A component preview system allows:

1. Viewing components with controlled props
2. Testing responsive behavior at specific widths
3. Comparing variants side-by-side
4. Iterating on styles without full app reload

Components export a standard interface: metadata (name, description, category), propTypes (type definitions with defaults), variants (pre-configured prop sets), and a render function.

Components that qualify are isolated, stateless render functions: row items, cards, badges, form inputs, buttons, section headers. Components that don't qualify have external dependencies or require lifecycle management.

### [UT12] Width-Controlled Responsive Testing.

Test responsive behavior by controlling container width, not viewport width:

```javascript
const preview = document.createElement('div');
preview.style.width = `${this.previewWidth}px`;
preview.appendChild(component.render(props));
```

Container width is preferred over viewport width because it enables faster iteration (no window resizing), precise control (exact pixel values), side-by-side comparison (same viewport, different widths), and component-level testing.

Provide slider + input + auto button for width control. Test components at key widths to understand wrapping behavior and document where natural breakpoints occur.

### [UT13] Variant-Based Testing.

Variants are pre-configured prop sets that represent meaningful states:

```javascript
export const variants = [
  { name: 'empty', props: { items: [], loading: false } },
  { name: 'loading', props: { items: [], loading: true } },
  { name: 'populated', props: { items: sampleItems, loading: false } }
];
```

Include variants for: default state (baseline/empty props), populated states (realistic sample data), edge cases (long text, empty data, error states), visual states (selected, hover, disabled), and responsive stress tests (maximum content that might wrap).

Variants serve as both documentation and test cases.

### [UT14] Responsive Design Strategy.

When building responsive components:

1. **Start with natural flow**: Use `flex-wrap: wrap` and let content flow naturally
2. **Measure natural breakpoints**: Use width control to find where content wraps
3. **Decide: natural vs controlled**: Natural wrapping (flex-wrap) is simpler and adapts to any content length but has less predictable visual rhythm. Controlled breakpoints (container queries) give explicit layout changes and predictable visual states but require more CSS complexity.
4. **Test with variants**: Create variants that stress-test wrapping with long content
5. **Document decisions**: Record breakpoint decisions in component or docs

```javascript
// Responsive behavior:
// < 200px: metrics stack vertically
// 200-280px: metrics wrap to 2 lines
// > 280px: single line
```

### [UT15] Claude Code Browser Automation.

Use Playwright MCP to give Claude Code direct control over a browser window. This enables interactive testing, responsive layout verification, and visual debugging without leaving the conversation.

**Setup**: Install with `claude mcp add playwright npx '@playwright/mcp@latest'`. Restart Claude Code after installation.

**Usage**: Direct Claude Code with natural language: "Use playwright mcp to open a browser to localhost:8000", "Resize the viewport to 600px wide", "Take a screenshot", "Click the Settings tab".

**Capabilities**: Navigation (open URLs, go back/forward, reload), viewport (resize, emulate devices), interaction (click, type, scroll, hover), inspection (screenshots, read content), forms (fill, select, submit), waiting (wait for elements, network idle).

**Responsive testing workflow**: Open the page, test wide layout (1200px), test narrow layout (400px), verify interactions, check navigation.

MCP turns browser testing from "write a script and run it" into an interactive conversation where Claude can observe results and adapt.
