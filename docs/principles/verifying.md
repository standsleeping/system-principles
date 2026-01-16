# Verifying

These principles govern how we verify correctness: testing strategies and mocking boundaries. Good tests evaluate design quality and focus on boundaries.

## Testing Principles

Testing is critical and often informs how subsystems are designed.

### [T1] Tests evaluate design quality.

Well-designed components produce tests that are easy to read, write, and run. We use our tests as a way of evaluating the quality of our design.

### [T2] Test-first approach.

Follow a strict test-first approach, always discussing WHAT behavior to test before determining HOW to test it. Never write code until tests have been written.

### [T3] Flat test structure.

Almost never use test classes; usually functions are simple and sufficiently "unit-like" that a flat list of pytest tests in a file will suffice.

### [T4] Declarative test documentation.

Tests are written before implementation with declarative assertion documentation. BAD: "Tests that env is loaded in non-containerized environment". GOOD: "Loads env in non-containerized environment".

### [T5] Centralized fixtures.

Fixtures are ALWAYS centralized and shared in `tests/fixtures.py`. No exceptions.

### [T6] Functional testing patterns.

Tests focus on input/output pairs for our functional codebase. Single pytest assertion per test where possible. Never patch/mock/stub code.

## Mocking Rules

Mocking should be limited to external boundaries. When tests require mocking application code, it signals a design problem.

### [MR1] Never mock application code.

Do not patch or fake your own functions, units, or integrators. Instead, run real code paths and only mock external boundaries. When tests would patch internal code, either refactor the code into units and integrators to make it more directly testable, or write integration tests that exercise the real code paths.

### [MR2] Mock only external boundaries.

External system boundaries (HTTP, filesystem, environment variables, databases) must be mocked for reliable, deterministic testing. Use helpers in `boundaries.py` to simulate HTTP, filesystem, environment, and session state. Keep your domain logic real.

### [MR3] No unittest.mock in tests.

Never import or use `unittest.mock` directly in test files. Never use `AsyncMock`, `MagicMock`, `patch`, or similar manual mocking. Use boundary helpers that encapsulate mocking instead.

### [MR4] Use boundary mockers for endpoints and translators.

Use `TestClient` from `starlette.testclient` for API endpoint testing. Use boundary mockers from `tests/boundaries.py`: `mock_http()` for HTTP requests, `mock_session()` for Starlette sessions, `mock_filesystem()` for file operations, `mock_env()` for environment variables, `mock_boundaries()` for comprehensive boundary mocking.

### [MR5] Mocking indicates design problems.

If your tests need to patch application code, refactor the design. Extract units (pure functions) and integrators (assemblers) so they are directly testable. Move side effects to explicit boundary adapters invoked by actions. Represent outcomes with result types instead of exceptions to simplify testing.
