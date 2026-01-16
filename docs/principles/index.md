# Principles Index

Quick reference for all tagged principles. Click any tag to jump to its full description.

Organized by activity: from how to think about systems, through modeling and structuring, to implementation, verification, and presentation.

---

## Designing

How to think about systems: philosophy and mental models.

### Boundaries (BD)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [BD1](designing.md#bd1-start-simple-add-useful-complexity) | Start simple, add useful complexity | Begin minimal; add complexity only when it improves the model |
| [BD2](designing.md#bd2-structure-reflects-sources-of-change) | Structure reflects sources of change | Organize code around what changes, not workflow |
| [BD3](designing.md#bd3-only-two-types-of-change-provide-more-require-less) | Only two types of change: provide more, require less | Evolve by strengthening outputs or relaxing inputs |
| [BD4](designing.md#bd4-a-module-is-a-hidden-decision) | A module is a hidden decision | Modules hide assumptions that might change |
| [BD5](designing.md#bd5-design-is-not-workflow) | Design is not workflow | Design around concepts, not execution order |
| [BD6](designing.md#bd6-framework-for-design) | Framework for design | Identify, isolate, and decouple sources of change |

### Abstraction (AB)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [AB1](designing.md#ab1-see-entanglement-not-hiding) | See entanglement, not hiding | Abstraction is about separating intertwined concerns |
| [AB2](designing.md#ab2-untangle-the-six-aspects) | Untangle the six aspects | Separate who, what, when, where, why, and how |
| [AB3](designing.md#ab3-reduce-interleaving-to-simplify) | Reduce interleaving to simplify | Simplicity is objectively measured by reduced coupling |
| [AB4](designing.md#ab4-test-simplicity-by-reassembly) | Test simplicity by reassembly | If parts reassemble easily, the design is simple |

### Cognitive Load (CL)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [CL1](designing.md#cl1-use-working-memory-as-your-complexity-limit) | Use working memory as your complexity limit | Keep concepts within what you can hold in mind |
| [CL2](designing.md#cl2-name-the-aspects-to-pull-them-apart) | Name the aspects to pull them apart | Naming who/what/when/where/why/how enables separation |

### Change (CH)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [CH1](designing.md#ch1-allow-only-accretion-and-relaxation) | Allow only accretion and relaxation | Only add capabilities or loosen requirements |
| [CH2](designing.md#ch2-never-mutate-create-new-with-new-names) | Never mutate; create new with new names | Coexist old and new; remove old at 100% adoption |
| [CH3](designing.md#ch3-provide-more-by-strengthening-outputs) | Provide more by strengthening outputs | Add guarantees, richer data, stronger postconditions |
| [CH4](designing.md#ch4-require-less-by-relaxing-inputs) | Require less by relaxing inputs | Accept broader inputs, fewer required fields |

### Logic (LG)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [LG1](designing.md#lg1-do-not-store-knowledge-as-control-flow) | Do not store knowledge as control flow | Each `if` encodes an assumption; avoid scattering them |
| [LG2](designing.md#lg2-hoist-decisions-toward-rule-sets) | Hoist decisions toward rule sets | Pull conditionals up until they become configuration |
| [LG3](designing.md#lg3-treat-decisions-as-data) | Treat decisions as data | Decisions as data defer commitment and reduce paths |
| [LG4](designing.md#lg4-encode-predicates-in-the-model) | Encode predicates in the model | Embed `if` conditions in types, invariants, or state machines |

---

## Modeling

Representing domain: data, types, and state.

### Values (VL)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [VL1](modeling.md#vl1-depend-on-values-not-behaviors) | Depend on values, not behaviors | Pass data between components, not method calls |
| [VL2](modeling.md#vl2-state-entangles-values-and-time) | State entangles values and time | State complicates by coupling what with when |

### Events (EV)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [EV1](modeling.md#ev1-store-facts-with-time) | Store facts with time | Facts need entity, attribute, value, time, and operation |

### Effects (EF)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [EF1](modeling.md#ef1-capture-time-dependent-results-explicitly) | Capture time-dependent results explicitly | When timing affects outcome, use explicit result types |

### Type Design (TD)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [TD1](modeling.md#td1-make-illegal-states-unrepresentable) | Make illegal states unrepresentable | Shrink representable state space to only valid states |
| [TD2](modeling.md#td2-chase-runtime-checks-upstream) | Chase runtime checks upstream | Push validation to boundaries for cleaner APIs |
| [TD3](modeling.md#td3-strengthen-inputs-dont-weaken-outputs) | Strengthen inputs, don't weaken outputs | Prefer `NonEmptyList[T] -> T` over `list[T] -> T | None` |
| [TD4](modeling.md#td4-types-as-module-boundaries) | Types as module boundaries | Public interfaces defined through data types |
| [TD5](modeling.md#td5-use-enums-over-booleans) | Use enums over booleans | Enums capture actual domain states; bools hide them |
| [TD6](modeling.md#td6-include-temporal-information) | Include temporal information | Track when facts became true, not just that they are |
| [TD7](modeling.md#td7-match-type-precision-to-stability) | Match type precision to stability | Loose types near volatility; precise types in stable core |

### Type Patterns (TP)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [TP1](modeling.md#tp1-avoid-returning-bool) | Avoid returning bool | Return evidence (validated result, error details) not yes/no |
| [TP2](modeling.md#tp2-acceptable-bools) | Acceptable bools | Pure predicates only: `is_empty`, `is_prime`, `is_even` |
| [TP3](modeling.md#tp3-validate-at-boundaries) | Validate at boundaries | Push validation to system edges, not scattered throughout |
| [TP4](modeling.md#tp4-refined-types-propagate-proofs) | Refined types propagate proofs | Once validated, the type carries the proof forward |
| [TP5](modeling.md#tp5-pattern-match-to-refine) | Pattern match to refine | Matching on sum types lets the compiler track information |
| [TP6](modeling.md#tp6-fix-the-upstream-type) | Fix the upstream type | If you need to cast, the source type is wrong |
| [TP7](modeling.md#tp7-use-runtime-narrowing) | Use runtime narrowing | Use `isinstance()` to narrow loose types, not `cast()` |
| [TP8](modeling.md#tp8-parse-into-stronger-types) | Parse into stronger types | Return proof-carrying values, not booleans |

### Type Syntax (TS)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [TS1](modeling.md#ts1-built-in-generic-types) | Built-in generic types | Use `list[T]`, `dict[K, V]`, not `List[T]`, `Dict[K, V]` |
| [TS2](modeling.md#ts2-union-syntax) | Union syntax | Use `T | None`, not `Optional[T]` |
| [TS3](modeling.md#ts3-generic-classes) | Generic classes | Use `class Foo[T]:`, not `TypeVar` + `Generic[T]` |
| [TS4](modeling.md#ts4-import-minimization) | Import minimization | Minimize `typing` imports; built-ins and `|` suffice |
| [TS5](modeling.md#ts5-domain-type-safety) | Domain type safety | No `dict[str, Any]` in domain; use Result types |

### Data Interchange (DDI)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [DDI1](modeling.md#ddi1-use-typeddict-for-interchange) | Use TypedDict for interchange | TypedDict for JSON, API requests, database rows |
| [DDI2](modeling.md#ddi2-use-dataclasses-for-domain) | Use Dataclasses for domain | Dataclasses for business entities with invariants |
| [DDI3](modeling.md#ddi3-translators-bridge-the-gap) | Translators bridge the gap | Parse TypedDict to Dataclass at boundaries |

---

## Structuring

Organizing code: architecture, boundaries, and modules.

### State & Architecture (SA)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [SA1](structuring.md#sa1-stateless-design) | Stateless design | All computations pure; no in-memory state |
| [SA2](structuring.md#sa2-event-sourcing) | Event sourcing | Events document behavior; entities compose from event streams |
| [SA3](structuring.md#sa3-database-as-truth) | Database as truth | Reads via queries; writes append events |
| [SA4](structuring.md#sa4-traceability) | Traceability | Compose SQL queries for audit trails and debugging |
| [SA5](structuring.md#sa5-time-travel) | Time travel | All state rewindable via events; no mutations |

### Project Structure (PS)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [PS1](structuring.md#ps1-data-structures-at-root) | Data structures at root | Types at package root; they define the vocabulary |
| [PS2](structuring.md#ps2-functions-in-subdirectory) | Functions in subdirectory | Functions in `functions/` folder, operating on root types |
| [PS3](structuring.md#ps3-the-111-rule) | The 1:1:1 Rule | One data structure, one function, one test suite per file |

### Code Building Blocks (CB)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [CB1](structuring.md#cb1-actions) | Actions | Entry points that accept requests and return typed results |
| [CB2](structuring.md#cb2-integrators) | Integrators | Assemble complex data by calling units/integrators |
| [CB3](structuring.md#cb3-units) | Units | Pure functions with simple data in and out |
| [CB4](structuring.md#cb4-translators) | Translators | Convert external data to domain types at boundaries |

### Boundary Types (BT)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [BT1](structuring.md#bt1-typeddict-at-boundaries) | TypedDict at boundaries | Never `dict[str, Any]`; use TypedDict for JSON shape |
| [BT2](structuring.md#bt2-translator-functions) | Translator functions | Standard pattern for external-to-domain conversion |
| [BT3](structuring.md#bt3-pure-conversion-only) | Pure conversion only | Translators convert types; no domain operations |

### Translators (TL)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [TL1](structuring.md#tl1-translators-only-convert-never-operate) | Translators only convert, never operate | Transform types; never call domain logic |
| [TL2](structuring.md#tl2-return-explicit-error-values) | Return explicit error values | Return typed errors, don't raise exceptions |
| [TL3](structuring.md#tl3-validate-structure-not-business-rules) | Validate structure, not business rules | Check shape and format; policy checks belong elsewhere |
| [TL4](structuring.md#tl4-unit-translators-are-self-contained) | Unit translators are self-contained | Direct transformation with no dependencies |
| [TL5](structuring.md#tl5-integrator-translators-compose-unit-translators) | Integrator translators compose unit translators | Complex translations assemble from simple ones |
| [TL6](structuring.md#tl6-chain-translators-with-explicit-error-propagation) | Chain translators with explicit error propagation | Errors flow through the chain explicitly |
| [TL7](structuring.md#tl7-one-translator-per-boundary-type) | One translator per boundary type | Separate translators for each external format |
| [TL8](structuring.md#tl8-domain--external-uses-domain-language) | Domain → External uses domain language | Outbound translators speak the domain's terms |
| [TL9](structuring.md#tl9-cross-domain-translators-enforce-boundary-rules) | Cross-domain translators enforce boundary rules | Inter-domain translators apply boundary constraints |
| [TL10](structuring.md#tl10-inject-translators-into-boundary-components) | Inject translators into boundary components | Pass translators as dependencies |
| [TL11](structuring.md#tl11-use-translators-in-request-handlers) | Use translators in request handlers | Convert at handler entry, not deep in logic |
| [TL12](structuring.md#tl12-keep-translator-error-types-consistent) | Keep translator error types consistent | Uniform error types across all translators |

---

## Implementing

Writing code: patterns, style, and dispatch.

### Polymorphism & Dispatch (PD)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [PD1](implementing.md#pd1-separate-decisions-from-behavior) | Separate decisions from behavior | Keep what-to-do apart from when-to-do-it |
| [PD2](implementing.md#pd2-prefer-data-driven-dispatch-for-evolving-domain-logic) | Prefer data-driven dispatch for evolving domain logic | Tables of handlers enable independent evolution |
| [PD3](implementing.md#pd3-use-in-place-pattern-matching-only-at-boundaries-or-tiny-stable-sets) | Use in-place pattern matching only at boundaries or tiny, stable sets | Match statements only for small, unchanging cases |
| [PD4](implementing.md#pd4-use-à-la-carte-polymorphism-for-extensibility) | Use à la carte polymorphism for extensibility | Protocols enable adding behaviors without changing types |
| [PD5](implementing.md#pd5-decisions-as-data) | Decisions as data | Dispatch tables are data that can be tested and extended |
| [PD6](implementing.md#pd6-keep-dependencies-out-of-dispatch-tables) | Keep dependencies out of dispatch tables | Tables should be pure mappings; inject deps at call site |
| [PD7](implementing.md#pd7-manage-exhaustiveness-explicitly) | Manage exhaustiveness explicitly | Verify all cases covered when dispatch tables change |
| [PD8](implementing.md#pd8-data-driven-dispatch-for-domain-logic) | Data-driven dispatch for domain logic | Handler tables separate decisions from behavior |

### Style Rules (SR)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [SR1](implementing.md#sr1-functional-programming-patterns) | Functional programming patterns | Pure functions, composition, no mutation |
| [SR2](implementing.md#sr2-python-language-usage) | Python language usage | Modern Python 3.13+; prefer `|` unions, generic syntax |

---

## Verifying

Testing and validation.

### Testing Principles (T)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [T1](verifying.md#t1-tests-evaluate-design-quality) | Tests evaluate design quality | Easy tests indicate good design |
| [T2](verifying.md#t2-test-first-approach) | Test-first approach | Define behavior before implementation |
| [T3](verifying.md#t3-flat-test-structure) | Flat test structure | Flat pytest functions; avoid test classes |
| [T4](verifying.md#t4-declarative-test-documentation) | Declarative test documentation | Name tests as facts: "Loads env..." not "Tests that..." |
| [T5](verifying.md#t5-centralized-fixtures) | Centralized fixtures | All fixtures in `tests/fixtures.py` |
| [T6](verifying.md#t6-functional-testing-patterns) | Functional testing patterns | Input/output pairs; single assertion per test |

### Mocking Rules (MR)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [MR1](verifying.md#mr1-never-mock-application-code) | Never mock application code | Refactor or use integration tests instead |
| [MR2](verifying.md#mr2-mock-only-external-boundaries) | Mock only external boundaries | HTTP, filesystem, env vars, databases only |
| [MR3](verifying.md#mr3-no-unittestmock-in-tests) | No unittest.mock in tests | Never use `patch`, `MagicMock`, `AsyncMock` |
| [MR4](verifying.md#mr4-use-boundary-mockers-for-endpoints-and-translators) | Use boundary mockers for endpoints and translators | Use `mock_http()`, `mock_session()`, etc. from `boundaries.py` |
| [MR5](verifying.md#mr5-mocking-indicates-design-problems) | Mocking indicates design problems | Need to mock signals poor architectural boundaries |

---

## Presenting

UI concerns: layout, visual design, and tooling.

### Layout (LY)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [LY1](presenting.md#ly1-no-page-level-scrolling) | No Page-Level Scrolling | Document body never scrolls; only regions scroll |
| [LY2](presenting.md#ly2-viewport-locked-containers) | Viewport-Locked Containers | Root containers fill exactly 100vh/100vw |
| [LY3](presenting.md#ly3-fixed-and-flexible-regions) | Fixed and Flexible Regions | Combine fixed headers with flexible content areas |
| [LY4](presenting.md#ly4-scroll-containment) | Scroll Containment | Each scrollable region manages its own overflow |
| [LY5](presenting.md#ly5-boundary-ownership) | Boundary Ownership | Components own their own visual boundaries |
| [LY6](presenting.md#ly6-empty-state-collapse) | Empty State Collapse | Empty containers collapse to zero height |
| [LY7](presenting.md#ly7-layout-variants) | Layout Variants | Responsive layouts switch between defined variants |
| [LY8](presenting.md#ly8-never-calculate-what-layout-can-handle) | Never Calculate What Layout Can Handle | Let CSS handle sizing; avoid JS calculations |
| [LY9](presenting.md#ly9-beware-common-layout-quirks) | Beware Common Layout Quirks | Inline-block gaps, 100vw scrollbar, margin collapse |

### Visual Design (VD)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [VD1](presenting.md#vd1-typography-based-hierarchy) | Typography-Based Hierarchy | Use font size/weight for hierarchy, not decoration |
| [VD2](presenting.md#vd2-transparent-by-default) | Transparent by Default | Elements transparent unless background is intentional |
| [VD3](presenting.md#vd3-minimal-borders) | Minimal Borders | Prefer spacing over borders; use sparingly |
| [VD4](presenting.md#vd4-spacing-strategy) | Spacing Strategy | Consistent spacing scale; fewer unique values |
| [VD5](presenting.md#vd5-color-usage) | Color Usage | Limited palette; color has semantic meaning |
| [VD6](presenting.md#vd6-simplification-patterns) | Simplification Patterns | Remove until it breaks; then add back minimally |
| [VD7](presenting.md#vd7-focus-states) | Focus States | Clear, consistent focus indicators for accessibility |
| [VD8](presenting.md#vd8-token-driven-design) | Token-Driven Design | Use design tokens for all values |
| [VD9](presenting.md#vd9-reset-first-approach) | Reset-First Approach | Reset browser defaults; build up from neutral base |
| [VD10](presenting.md#vd10-responsive-component-design) | Responsive Component Design | Information hierarchy and graceful width degradation |
| [VD11](presenting.md#vd11-data-ink-ratio-and-tabular-alignment) | Data-Ink Ratio and Tabular Alignment | Deduplicate labels; align numbers for scanability |
| [VD12](presenting.md#vd12-one-signal-per-meaning) | One Signal Per Meaning | Each meaning communicated through one visual channel |

### Tooling (UT)

| Tag | Principle | Summary |
|-----|-----------|---------|
| [UT1](presenting.md#ut1-automatic-verification) | Automatic Verification | Automated checks for layout and overflow issues |
| [UT2](presenting.md#ut2-overflow-detection) | Overflow Detection | Detect and report content exceeding containers |
| [UT3](presenting.md#ut3-ancestry-tracing) | Ancestry Tracing | Trace element ancestry to find layout violations |
| [UT4](presenting.md#ut4-visual-debugging) | Visual Debugging | Overlay tools to visualize layout structure |
| [UT5](presenting.md#ut5-test-integration) | Test Integration | Layout verification in automated tests |
| [UT6](presenting.md#ut6-development-workflow) | Development Workflow | Immediate feedback during development |
| [UT7](presenting.md#ut7-diagnostic-output) | Diagnostic Output | Clear, actionable diagnostic messages |
| [UT8](presenting.md#ut8-continuous-monitoring) | Continuous Monitoring | Watch for regressions over time |
| [UT9](presenting.md#ut9-presenting-results-to-users) | Presenting Results to Users | User-friendly result presentation |
| [UT10](presenting.md#ut10-headless-console-debugging) | Headless Console Debugging | Debug layout without visual browser |
| [UT11](presenting.md#ut11-component-preview-systems) | Component Preview Systems | Isolated component preview environments |
| [UT12](presenting.md#ut12-width-controlled-responsive-testing) | Width-Controlled Responsive Testing | Test at specific viewport widths |
| [UT13](presenting.md#ut13-variant-based-testing) | Variant-Based Testing | Test all component variants systematically |
| [UT14](presenting.md#ut14-responsive-design-strategy) | Responsive Design Strategy | Structured approach to responsive breakpoints |
| [UT15](presenting.md#ut15-claude-code-browser-automation) | Claude Code Browser Automation | Automated browser testing with Claude Code |

---

## Summary

| Section | Subsections | Principles |
|---------|-------------|------------|
| Designing | 5 | 20 |
| Modeling | 7 | 27 |
| Structuring | 5 | 27 |
| Implementing | 2 | 10 |
| Verifying | 2 | 11 |
| Presenting | 3 | 36 |
| **Total** | **24** | **131** |

---

## Alternative Taxonomy: By Core Concept

For future consideration, here's how these principles could be organized by concept rather than activity:

| Section | Subsections |
|---------|-------------|
| **Simplicity** | Abstraction (AB), Cognitive Load (CL) |
| **Change** | Change (CH), Boundaries (BD) |
| **Logic** | Logic (LG) |
| **Data** | Values (VL), Events (EV), Effects (EF) |
| **Types** | Type Design (TD), Type Patterns (TP), Type Syntax (TS), Data Interchange (DDI) |
| **Boundaries** | Boundary Types (BT), Translators (TL) |
| **Structure** | State & Architecture (SA), Project Structure (PS), Code Building Blocks (CB) |
| **Dispatch** | Polymorphism & Dispatch (PD) |
| **Style** | Style Rules (SR) |
| **Testing** | Testing Principles (T), Mocking Rules (MR) |
| **UI** | Layout (LY), Visual Design (VD), Tooling (UT) |

This groups by "what the principle is about" rather than "when you'd use it."
