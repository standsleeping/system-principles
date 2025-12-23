# Principles Index

Quick reference for all tagged principles. Click any tag to jump to its full description.

Organized from foundational design principles to specific implementation patterns, with UI principles at the end.

---

## Projects

### State & Architecture (SA)

| Tag | Principle |
|-----|-----------|
| [SA1](projects.md#sa1-stateless-design) | Stateless design |
| [SA2](projects.md#sa2-event-sourcing) | Event sourcing |
| [SA3](projects.md#sa3-database-as-truth) | Database as truth |
| [SA4](projects.md#sa4-traceability) | Traceability |
| [SA5](projects.md#sa5-time-travel) | Time travel |

### Type-First Design (TFD)

| Tag | Principle |
|-----|-----------|
| [TFD1](projects.md#tfd1-types-as-module-boundaries) | Types as module boundaries |

### Project Structure (PS)

| Tag | Principle |
|-----|-----------|
| [PS1](projects.md#ps1-data-structures-at-root) | Data structures at root |
| [PS2](projects.md#ps2-functions-in-subdirectory) | Functions in subdirectory |
| [PS3](projects.md#ps3-the-111-rule) | The 1:1:1 Rule |

### Code Building Blocks (CB)

| Tag | Principle |
|-----|-----------|
| [CB1](projects.md#cb1-actions) | Actions |
| [CB2](projects.md#cb2-integrators) | Integrators |
| [CB3](projects.md#cb3-units) | Units |
| [CB4](projects.md#cb4-translators) | Translators |

### Style Rules (SR)

| Tag | Principle |
|-----|-----------|
| [SR1](projects.md#sr1-functional-programming-patterns) | Functional programming patterns |
| [SR2](projects.md#sr2-python-language-usage) | Python language usage |

---

## Polymorphism & Dispatch (PD)

| Tag | Principle |
|-----|-----------|
| [PD1](polymorphism.md#pd1-separate-decisions-from-behavior) | Separate decisions from behavior |
| [PD2](polymorphism.md#pd2-prefer-data-driven-dispatch-for-evolving-domain-logic) | Prefer data-driven dispatch for evolving domain logic |
| [PD3](polymorphism.md#pd3-use-in-place-pattern-matching-only-at-boundaries-or-tiny-stable-sets) | Use in-place pattern matching only at boundaries or tiny, stable sets |
| [PD4](polymorphism.md#pd4-use-a-la-carte-polymorphism-for-extensibility) | Use à la carte polymorphism for extensibility |
| [PD5](polymorphism.md#pd5-decisions-as-data) | Decisions as data |
| [PD6](polymorphism.md#pd6-keep-dependencies-out-of-dispatch-tables) | Keep dependencies out of dispatch tables |
| [PD7](polymorphism.md#pd7-manage-exhaustiveness-explicitly) | Manage exhaustiveness explicitly |

---

## Typing

### Function Return Expectations (FRE)

| Tag | Principle |
|-----|-----------|
| [FRE1](typing.md#fre1-avoid-returning-bool) | Avoid returning bool |
| [FRE2](typing.md#fre2-acceptable-bools) | Acceptable bools |

### Type-Checked Proofs (TCP)

| Tag | Principle |
|-----|-----------|
| [TCP1](typing.md#tcp1-validate-at-boundaries) | Validate at boundaries |
| [TCP2](typing.md#tcp2-refined-types-propagate-proofs) | Refined types propagate proofs |
| [TCP3](typing.md#tcp3-pattern-match-to-refine) | Pattern match to refine |

### Narrowing Casts (NC)

| Tag | Principle |
|-----|-----------|
| [NC1](typing.md#nc1-fix-the-upstream-type) | Fix the upstream type |
| [NC2](typing.md#nc2-use-runtime-narrowing) | Use runtime narrowing |

### Data & Domain Interchange (DDI)

| Tag | Principle |
|-----|-----------|
| [DDI1](typing.md#ddi1-use-typeddict-for-interchange) | Use TypedDict for interchange |
| [DDI2](typing.md#ddi2-use-dataclasses-for-domain) | Use Dataclasses for domain |
| [DDI3](typing.md#ddi3-translators-bridge-the-gap) | Translators bridge the gap |

### Explicit State Modeling (ESM)

| Tag | Principle |
|-----|-----------|
| [ESM1](typing.md#esm1-use-enums-over-booleans) | Use enums over booleans |
| [ESM2](typing.md#esm2-include-temporal-information) | Include temporal information |

### State-Driven Branching (SDB)

| Tag | Principle |
|-----|-----------|
| [SDB1](typing.md#sdb1-data-driven-dispatch-for-domain-logic) | Data-driven dispatch for domain logic |

### Type Rules (TR)

| Tag | Principle |
|-----|-----------|
| [TR1](projects.md#tr1-built-in-generic-types) | Built-in generic types |
| [TR2](projects.md#tr2-union-syntax) | Union syntax |
| [TR3](projects.md#tr3-generic-classes) | Generic classes |
| [TR4](projects.md#tr4-import-minimization) | Import minimization |
| [TR5](projects.md#tr5-domain-type-safety) | Domain type safety |
| [TR6](projects.md#tr6-no-casting) | No casting |

---

## Translators

### Pure Boundary Conversion (PBC)

| Tag | Principle |
|-----|-----------|
| [PBC1](translators.md#pbc1-translators-only-convert-never-operate) | Translators only convert, never operate |
| [PBC2](translators.md#pbc2-return-explicit-error-values) | Return explicit error values |
| [PBC3](translators.md#pbc3-validate-structure-not-business-rules) | Validate structure, not business rules |

### Translator Composition (TC)

| Tag | Principle |
|-----|-----------|
| [TC1](translators.md#tc1-unit-translators-are-self-contained) | Unit translators are self-contained |
| [TC2](translators.md#tc2-integrator-translators-compose-unit-translators) | Integrator translators compose unit translators |
| [TC3](translators.md#tc3-chain-translators-with-explicit-error-propagation) | Chain translators with explicit error propagation |

### Boundary-Specific Translators (BST)

| Tag | Principle |
|-----|-----------|
| [BST1](translators.md#bst1-one-translator-per-boundary-type) | One translator per boundary type |
| [BST2](translators.md#bst2-domain-external-uses-domain-language) | Domain → External uses domain language |
| [BST3](translators.md#bst3-cross-domain-translators-enforce-boundary-rules) | Cross-domain translators enforce boundary rules |

### Boundary Types (BT)

| Tag | Principle |
|-----|-----------|
| [BT1](projects.md#bt1-typeddict-at-boundaries) | TypedDict at boundaries |
| [BT2](projects.md#bt2-translator-functions) | Translator functions |
| [BT3](projects.md#bt3-pure-conversion-only) | Pure conversion only |
| [BT4](projects.md#bt4-parse-into-stronger-types-dont-validate-to-booleans) | Parse into stronger types (don't validate to booleans) |

### Integration Patterns (IP)

| Tag | Principle |
|-----|-----------|
| [IP1](translators.md#ip1-inject-translators-into-boundary-components) | Inject translators into boundary components |
| [IP2](translators.md#ip2-use-translators-in-request-handlers) | Use translators in request handlers |
| [IP3](translators.md#ip3-keep-translator-error-types-consistent) | Keep translator error types consistent |

---

## Testing

### Testing Principles (T)

| Tag | Principle |
|-----|-----------|
| [T1](projects.md#t1-tests-evaluate-design-quality) | Tests evaluate design quality |
| [T2](projects.md#t2-test-first-approach) | Test-first approach |
| [T3](projects.md#t3-flat-test-structure) | Flat test structure |
| [T4](projects.md#t4-declarative-test-documentation) | Declarative test documentation |
| [T5](projects.md#t5-centralized-fixtures) | Centralized fixtures |
| [T6](projects.md#t6-functional-testing-patterns) | Functional testing patterns |

### Mocking Rules (MR)

| Tag | Principle |
|-----|-----------|
| [MR1](mocking.md#mr1-never-mock-application-code) | Never mock application code |
| [MR2](mocking.md#mr2-mock-only-external-boundaries) | Mock only external boundaries |
| [MR3](mocking.md#mr3-no-unittestmock-in-tests) | No unittest.mock in tests |
| [MR4](mocking.md#mr4-use-boundary-mockers-for-endpoints-and-translators) | Use boundary mockers for endpoints and translators |
| [MR5](mocking.md#mr5-mocking-indicates-design-problems) | Mocking indicates design problems |

---

## UI: Layout (LY)

| Tag | Principle |
|-----|-----------|
| [LY1](layout.md#ly1-no-page-level-scrolling) | No Page-Level Scrolling |
| [LY2](layout.md#ly2-viewport-locked-containers) | Viewport-Locked Containers |
| [LY3](layout.md#ly3-fixed-and-flexible-regions) | Fixed and Flexible Regions |
| [LY4](layout.md#ly4-scroll-containment) | Scroll Containment |
| [LY5](layout.md#ly5-container-boundary-rule) | Container Boundary Rule |
| [LY6](layout.md#ly6-empty-state-collapse) | Empty State Collapse |
| [LY7](layout.md#ly7-layout-variants) | Layout Variants |
| [LY8](layout.md#ly8-never-calculate-what-layout-can-handle) | Never Calculate What Layout Can Handle |

---

## UI: Visual Design (VD)

| Tag | Principle |
|-----|-----------|
| [VD1](visual-design.md#vd1-typography-based-hierarchy) | Typography-Based Hierarchy |
| [VD2](visual-design.md#vd2-transparent-by-default) | Transparent by Default |
| [VD3](visual-design.md#vd3-minimal-borders) | Minimal Borders |
| [VD4](visual-design.md#vd4-spacing-strategy) | Spacing Strategy |
| [VD5](visual-design.md#vd5-color-usage) | Color Usage |
| [VD6](visual-design.md#vd6-simplification-patterns) | Simplification Patterns |
| [VD7](visual-design.md#vd7-focus-states) | Focus States |
| [VD8](visual-design.md#vd8-token-driven-design) | Token-Driven Design |
| [VD9](visual-design.md#vd9-reset-first-approach) | Reset-First Approach |

---

## UI: Tooling (UT)

| Tag | Principle |
|-----|-----------|
| [UT1](ui-tooling.md#ut1-automatic-verification) | Automatic Verification |
| [UT2](ui-tooling.md#ut2-overflow-detection) | Overflow Detection |
| [UT3](ui-tooling.md#ut3-ancestry-tracing) | Ancestry Tracing |
| [UT4](ui-tooling.md#ut4-visual-debugging) | Visual Debugging |
| [UT5](ui-tooling.md#ut5-test-integration) | Test Integration |
| [UT6](ui-tooling.md#ut6-development-workflow) | Development Workflow |
| [UT7](ui-tooling.md#ut7-diagnostic-output) | Diagnostic Output |
| [UT8](ui-tooling.md#ut8-continuous-monitoring) | Continuous Monitoring |
| [UT9](ui-tooling.md#ut9-presenting-results-to-users) | Presenting Results to Users |
