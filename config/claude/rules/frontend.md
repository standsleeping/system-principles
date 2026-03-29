---
paths:
  - "**/*.html"
  - "**/*.css"
  - "**/*.js"
---

# Frontend Conventions

Follow these principles when writing or modifying HTML, CSS, or JavaScript.

## Layout
*Rules for visual layout and structure. Layout principles govern the structural arrangement of UI components: where content lives, what contains what, and how space is allocated.*

- **NO_PAGE_SCROLL** No Page-Level Scrolling.: If the page itself scrolls, something is wrong; scrolling is an intentional per-component decision.
- **VIEWPORT_LOCKED** Viewport-Locked Containers.: Lock the root to the viewport; from there, all scrolling must be explicitly delegated to content regions.
- **FIXED_FLEXIBLE_REGIONS** Fixed and Flexible Regions.: Fixed regions claim explicit space via tokens; flexible regions take whatever remains.
- **SCROLL_CONTAINMENT** Scroll Containment.: Only leaf content areas scroll; every container above them clips with overflow hidden.
- **BOUNDARY_OWNERSHIP** Boundary Ownership.: Each component should look visually complete in isolation; relying on a neighbor for your edge is implicit coupling.
- **EMPTY_STATE_COLLAPSE** Empty State Collapse.: Empty structural elements hide automatically, so optional slots can be omitted without leaving gaps.
- **LAYOUT_VARIANTS** Layout Variants.: One viewport-locked shell, many configurations: modifier classes adjust which regions appear and how space is distributed.
- **NEVER_CALC_LAYOUT** Never Calculate What Layout Can Handle.: Never hardcode a value that depends on another element's size. Use flexbox to let the browser distribute space automatically.
- **LAYOUT_QUIRKS** Beware Common Layout Quirks.: Mysterious layout gaps usually come from implicit CSS behaviors invisible in DevTools: baselines, 100vw, margin collapsing.
- **OVERFLOW_CAUSES** Common Overflow Causes.: When the no-scroll constraint is violated, common causes include viewport width issues, mismatched calculations, flex sizing, box-sizing, and missing overflow properties.
## Visual Design
*Rules for visual design and aesthetics. How interfaces look, how hierarchy is communicated, and how users perceive structure through typography, color, and spacing.*

- **RESET_FIRST** Reset-First Approach.: Strip all browser defaults; every margin and padding should be a deliberate choice.
- **TOKEN_DRIVEN_DESIGN** Token-Driven Design.: CSS variables are the single source of truth for design decisions: one change propagates everywhere.
- **TYPOGRAPHY_HIERARCHY** Typography-Based Hierarchy.: When weight and size establish hierarchy, color stays available for meaning like status and interaction.
- **SPACING_STRATEGY** Spacing Strategy.: Use flex gap for spacing between elements; it's more predictable and needs no last-child overrides.
- **COLOR_USAGE** Color Usage.: A restrained palette makes intentional color usage more impactful; reserve color for meaning.
- **SIMPLIFICATION_PATTERNS** Simplification Patterns.: Each visual element costs attention. Earn that cost.
- **ONE_SIGNAL_PER_MEANING** One Signal Per Meaning.: If you remove a visual treatment and the user loses no information, it was noise.
- **DATA_INK_RATIO** Data-Ink Ratio and Tabular Alignment.: Maximize information, minimize redundant visual elements; deduplicate labels and align values for scanability.
- **VISUAL_ENCODING** Visual Encoding vs. Text.: Text for precision, visual for shape; supplement, don't duplicate.
- **SUBORDINATE_VISUALIZATION** Subordinate Inline Visualization.: Inline visualizations annotate; they recede into the row, not headline it.
- **FOCUS_STATES** Focus States.: Every interactive element needs a visible, consistent focus indicator; keyboard users depend on it.
- **RESPONSIVE_COMPONENTS** Responsive Component Design.: Rank information by priority; lower-priority items hide before higher-priority items truncate.
## Ui Debugging
*Principles that guide how to effectively debug HTML/JS/CSS. Tools and techniques for verifying UI constraints, debugging layout issues, and maintaining visual consistency.*

- **AUTO_VERIFICATION** Automatic Verification.: Layout constraints should be automatically verified, not manually inspected. When a constraint like "no page-level scrolling" exists, tooling should:
- **DEV_WORKFLOW** Development Workflow.: Layout debugging should be always-on in development and enforced as build failures in CI.
- **CONTINUOUS_MONITORING** Continuous Monitoring.: One-time scans miss overflow that appears at certain sizes or after dynamic loads; watch continuously.
- **OVERFLOW_DETECTION** Overflow Detection.: Good overflow tooling identifies both the symptom (page scrolls) and the cause (which element).
- **ANCESTRY_TRACING** Ancestry Tracing.: The fix belongs on the ancestor where overflow starts, not the element that sticks out.
- **DIAGNOSTIC_OUTPUT** Diagnostic Output.: Diagnostics should tell you what failed, by how much, and which elements contribute.
- **PRESENT_RESULTS** Presenting Results to Users.: Show the math, visualize the spatial relationships, and highlight whether the constraint holds.
- **VISUAL_DEBUGGING** Visual Debugging.: Visual feedback makes layout problems apparent without opening DevTools.
- **TEST_INTEGRATION** Test Integration.: Layout constraints are testable assertions: automate them so violations fail the build.
- **HEADLESS_DEBUGGING** Headless Console Debugging.: JavaScript fails silently from the user's perspective; headless console checks catch what no visible error reveals.
- **COMPONENT_PREVIEW** Component Preview Systems.: If a component can't be rendered in isolation, it has too many dependencies on its context.
- **WIDTH_CONTROLLED_TESTING** Width-Controlled Responsive Testing.: Control container width, not viewport width: it's precise, fast, and allows side-by-side comparison.
- **VARIANT_BASED_TESTING** Variant-Based Testing.: Pre-configured prop sets serve as both living documentation and test cases for every meaningful state.
- **RESPONSIVE_STRATEGY** Responsive Design Strategy.: Start with natural flow, measure where it breaks, then decide whether to let it wrap or control it explicitly.
- **BROWSER_AUTOMATION** Claude Code Browser Automation.: MCP turns browser testing from writing scripts into an interactive conversation where results can be observed and adapted to.
