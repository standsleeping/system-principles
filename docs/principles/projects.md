# Projects

Principles for the overall system architecture, file structure, testing guidelines, and coding style should be studied closely.

Please also refer to README.md at the project root for details about the purpose of this project, how it is organized and configured, and for specific usage examples.

## Commands

Set up to run as a module:

```bash
uv pip install -e .
```

Always run `pytest` (and commands like `mypy` and `ty`) via `uv`:

```bash
uv run python -m pytest
```

## System Architecture

This project follows a strict "hexagonal" architecture (also known as "functional core, imperative shell" or "ports and adapters") with a type-driven development methodology.

The codebase is organized modularly, as a series of packages. Each package is designed as an independent unit with a clear, type-first API. Types serve as the primary contract between modules, complete with usage guidelines and documentation. Circular dependencies between packages are strictly forbidden.

Our primary design constraints and guiding principles are as follows.

### [SA1] Stateless design.

All computations are pure. No in-memory state anywhere.

### [SA2] Event sourcing.

Events are living documentation of system behaviors. Note that all "entites" or objects that appear as nouns are almost always _composed_ from streams of events.

### [SA3] Database as truth.

All reads go through SQL queries. All writes append events.

### [SA4] Traceability.

Easy audit trails are composed via the database. Composing a set of SQL queries to create a full picture of what happened is how 99% of bugs are found.

### [SA5] Time travel.

All state is rewindable via events. Think accounting and ledgers. No mutations!

## Type-First Development

In this architecture, types are the foundation of system design.

### [TFD1] Types as module boundaries.

Each package's public interface is defined primarily through its data types.

Development follows a type-first workflow, where data structures and types that model the domain are often designed first, with pure functions that transform these types are implemented next. Type signatures guide and constrain implementations.

The prohibition on circular dependencies is reinforced by our type system. Modules can only depend on types from their dependencies, creating a clear, unidirectional flow.

## Package Structure

Each package maintains a strict separation between functions and data.

### [PS1] Data structures at root.

Types and dataclasses are placed at the package root level, at the same level as the `functions` folder. This placement reflects their fundamental importance. In this architecture, data structures are of the utmost importance as they define the vocabulary of the system, help establish module boundaries, guide function implementations, and ensure type safety across module boundaries.

### [PS2] Functions in subdirectory.

Functions, wherever possible, are kept in the package's `functions` folder. These functions operate on the well-defined types, with their signatures serving as executable documentation of the transformations they perform.

### [PS3] The 1:1:1 Rule.

We maintain a strict 1:1 correspondence between:

1. **Data and files**: One data structure per file.
2. **Functions and files**: One function per file.
3. **Files and tests**: One file, one test suite.

Union types and their constituent result types may be grouped together in a single file when they form a cohesive set of related outcomes for a specific operation

Example: `RegistrationResult = RegistrationSuccess | AlreadyExists | InvalidAppData`.

At the same level as the functions and data, there may also exist subpackages with semantically meaningful names, themselves having the same data/function structure as the subpackage they are in.

## Boundaries and Translators

A critical aspect of hexagonal architecture is proper boundary management between layers.

### [BT1] No dict[str, Any] in domain.

When `dict[str, Any]` types propagate deeper into the codebase beyond initial entry points, boundaries are not properly defined. This causes:

- **Loss of type safety**: No IDE support, no compile-time checks, runtime errors.
- **Domain modeling failure**: Domain objects represent business concepts.
- **Scattered validation**: Without proper deserialization, validation spreads everywhere.
- **Coupling to transport**: Domain logic becomes coupled to JSON structure.

### [BT2] Translator functions.

Use translator functions as the standard pattern for converting external data (JSON, HTTP requests) into domain objects. These functions have a single, narrow responsibility:

- **Pure conversion**: Transform `dict[str, Any]` from requests into properly typed domain objects.
- **Boundary validation**: Handle conversion errors with appropriate HTTP responses.
- **No domain logic**: Never perform domain operations, only convert types and pass to domain!

### [BT3] Pure conversion only.

Translators must transform `dict[str, Any]` from requests into properly typed domain objects, handle conversion errors with appropriate HTTP responses, and never perform domain operations (only convert types and pass to domain layer).

See [translators.md](translators.md) for detailed implementation guidelines.

### [BT4] *Parse* into stronger types (don't *validate* to booleans)

Validation returns booleans; parsing returns stronger types that carry the proof forward.

- Translators SHOULD build context-free proofs: presence/shape, normalization, simple formats (UUID, ISO date, email syntax), and cross-field form invariants that require no I/O (e.g., password == confirm).
- Translators MUST NOT implement policy/stateful checks: uniqueness, invites, quotas/rate limits, time-based rules, or config-driven policies (e.g., password strength).
- Prefer strengthening inputs over weakening outputs: construct proof-carrying values (e.g., `EmailAddress`, `ConfirmedPassword`) and return a typed `...Input` object on success.
- Validators should look like parsers: return proof-carrying values, not booleans.

Acceptance checks:
- No domain function accepts raw transport primitives when a proof-carrying type exists.
- No boolean-returning `validate_*` helpers for boundary form checks remain; translators return typed values or structured errors.

## Testing

Testing is critical in this project and often informs how subsystems are designed.

### [T1] Tests evaluate design quality.

Well-designed components produce tests that are easy to read, write, and run. We use our tests as a way of evaluating the quality of our design.

### [T2] Test-first approach.

Follow a strict test-first approach, always discussing WHAT behavior to test before determining HOW to test it. Never write code until tests have been written.

### [T3] Flat test structure.

Almost never use test classes; usually functions are simple and sufficiently "unit-like" that a flat list of pytest tests in a file will suffice.

### [T4] Declarative test documentation.

Tests are written before implementation with declarative assertion documentation. BAD: "Tests that env is loaded in non-containerized environment". GOOD: "Loads env in non-containerized environment".

### [T5] Centralized fixtures.

Fixtures are ALWAYS centralized and shared in tests/fixtures.py. No exceptions.

### [T6] Functional testing patterns.

Tests focus on input/output pairs for our functional codebase. Single pytest assertion per test where possible. Never patch/mock/stub code (see below).

## Mocking

### [MR1] Never mock application code.

Avoid mocking our own application code. When tests would patch internal code, either: refactor the code into units and integrators to make it more directly testable, or write integration tests that exercise the real code paths without mocking.

### [MR2] Mock only external boundaries.

External system boundaries (HTTP, filesystem, environment variables, databases) must be mocked for reliable, deterministic testing. All boundary mocking should be centralized in `boundaries.py`.

### [MR3] No unittest.mock.

NEVER import or use `unittest.mock` directly in test files. NEVER use `AsyncMock`, `MagicMock`, `patch`, or similar manual mocking.

### [MR4] Use boundary mockers.

ALWAYS use `TestClient` from `starlette.testclient` for API endpoint testing. ALWAYS use boundary mockers from `tests/boundaries.py`: `mock_http()` for HTTP requests, `mock_session()` for Starlette sessions, `mock_filesystem()` for file operations, `mock_env()` for environment variables, `mock_boundaries()` for comprehensive boundary mocking.

### [MR5] Violations indicate design problems.

Violation of these mocking rules indicates poor architectural boundaries and must be fixed by refactoring to use proper fixtures and integration patterns.

## Core Building Blocks

Files will contain one (and only one, per file) of the following simple "building block" code types. This is the most commonly violated architectural rule; be rigorous in your assessment as to whether the code you produce adheres to these standards.

We avoid combinatorial explosion (2^n paths for n branches) through careful design that makes invalid states unrepresentable and maintains a clear separation between actions, integrators, and units.

### [CB1] Actions.

Accept a user's request, or specification of work, and return a result object. Characteristics:

- Entry point at a boundary: HTTP handler, CLI command, job runner, or scheduler tick.
- Accepts a user's request/specification and returns a typed result object.
- Uses translator functions to parse inputs and serialize outputs.
- Orchestrates units and integrators; contains no domain decisions itself.
- Performs side effects ONLY at boundaries.
- Valid boundary effects: transactions, appends events, enqueues jobs, logs/metrics/traces.
- Uses explicit control flow with early returns; avoids complex branching.
- Never raises to signal domain failures; returns typed results instead.

### [CB2] Integrators.

Assemble a complex structure or data type. They "glue together" different behaviors and produce composite data structures. Characteristics:

- Calls other units and/or integrators.
- Sole purpose is to assemble complex return types and data structures.
- Delegates to other unit/integrator calls.
- Never makes semantically meaningful decisions: always delegates to other integrators/units.
- Can use if/else but ONLY to conditionally (i.e. early) return its return type.
- Simple integration tests: one test function/suite-of-functions for each `return`.
- Size of test suite is proportional to variety of return conditions.
- Tests NEVER mock or stub user code; always RUNS code that integrator depends on.

### [CB3] Units.

Implement a simple, testable decision or calculation that the code makes. They are pure functions. Characteristics:

- Simple data types in and out.
- Pure functions, no imports, no dependencies, no side effects.
- Tested simply: all possible return values are covered in unit-like assertions.

### [CB4] Translators.

Translator functions (either units or integrators) sit at system or package boundaries, and can be either units or integrators, depending on the context.

**Translator as Unit:**

- Direct transformation of `dict[str, Any]` to domain types using only built-in functions.
- No dependencies: only standard library functions (uuid.UUID, datetime.fromisoformat, etc.).
- No imports: No calls to other application functions.
- Example: Converting string to UUID, parsing ISO datetime, basic type coercion.

**Translator as Integrator:**

- Composed conversion: Calls other units/integrators to perform complex translations.
- Has dependencies: Uses validation units, parsing integrators, or lookup functions.
- Assembles results: Combines multiple conversion operations into domain objects.
- Example: Converting request data that requires validation against existing domain rules.

**Both types:**

- Only convert: Transform external data to domain types.
- Only validate boundaries: Handle conversion errors and return appropriate error responses.
- Pass, don't execute: Return properly typed domain objects for other functions to use.
- No domain operations: Never call domain functions directly, leave that to the calling context.

## Style

### [SR1] Functional programming patterns.

- Prefer functions and composition over classes and inheritance.
- Functions are almost always pure and have no side effects.
- Functions follow SRP and are small/focused.
- Functions always have clear input and output types.
- Functions never mutate their arguments.

### [SR2] Python language usage.

- Always use `dedent` for multi-line strings.
- Avoid underscore method patterns; always prefer `this_func` over `_this_func`.
- Always prefer modern Python (3.13+) language and type features.
- Always use generic type parameter syntax (`class Foo[T]:` instead of `TypeVar`).
- Prefer union types with `|` syntax (`str | None` instead of `Union[str, None]`).
- Never use `if TYPE_CHECKING`.
- Never use `# type: ignore[xyz]`.

## Types

We always follow modern Python typing conventions and avoid legacy typing patterns.

### [TR1] Built-in generic types.

- Use: `list[T]`, `dict[K, V]`, `set[T]`, `tuple[T, ...]`
- Avoid: `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[T, ...]`

### [TR2] Union syntax.

- Use: `T | None`, `str | int`, `list[str] | dict[str, int]`
- Avoid: `Optional[T]`, `Union[str, int]`

### [TR3] Generic classes.

- Use: `class Container[T]:` (PEP 695 syntax)
- Avoid: `T = TypeVar('T')` + `class Container(Generic[T]):`

### [TR4] Import minimization.

- Only import from `typing` when necessary (e.g., `Any`, `Protocol`, `Literal`)
- Never import: `List`, `Dict`, `Set`, `Tuple`, `Optional`, `Union`, `Generic`, `TypeVar`
- Built-in types and union syntax eliminate most `typing` imports
- Use `type` statement for type aliases instead of `TypeAlias`

### [TR5] Domain type safety.

- Never allow `dict[str, Any]` in domain layers.
- Instead of raising exceptions in domain logic, use Result types.
- Result types make success and failure explicit.
- Handle errors explicitly, so all possible outcomes are visible in the type signature.
- Domain functions should never throw, making them predictable.
- Test both success and failure paths without exception handling.

## Progress

Some code in this project predates these rules and is not yet in compliance. Before making changes to existing functionality, please review the code and determine if it is in compliance with the rules. If it is not in compliance, please highlight the code in question and ask for guidance as to whether it should be changed before proceeding.
