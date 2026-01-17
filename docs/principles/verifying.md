# Verifying

These principles govern how we verify correctness: testing strategies and mocking boundaries. Good tests evaluate design quality and focus on boundaries.

## Testing Principles

Testing is critical and often informs how subsystems are designed.

### [T1] Tests evaluate design quality.

Well-designed components produce tests that are easy to read, write, and run. We use our tests as a way of evaluating the quality of our design.

### [T2] Test-first approach.

Follow a strict test-first approach, always discussing WHAT behavior to test before determining HOW to test it. Never write code until tests have been written.

### [T3] Declarative test documentation.

Tests are written before implementation with declarative assertion documentation. BAD: "Tests that env is loaded in non-containerized environment". GOOD: "Loads env in non-containerized environment".

### [T4] Functional testing patterns.

Tests focus on input/output pairs for our functional codebase. Single assertion per test where possible. Never patch/mock/stub code.

## Mocking Rules

Mocking should be limited to external boundaries. When tests require mocking application code, it signals a design problem.

### [MR1] Never mock application code.

Do not patch or fake your own functions, units, or integrators. Instead, run real code paths and only mock external boundaries. When tests would patch internal code, either refactor the code into units and integrators to make it more directly testable, or write integration tests that exercise the real code paths.

### [MR2] Mock only external boundaries.

External system boundaries (HTTP, filesystem, environment variables, databases) must be mocked for reliable, deterministic testing. Use helpers in `boundaries.py` to simulate HTTP, filesystem, environment, and session state. Keep your domain logic real.

### [MR3] Use purpose-built boundary test doubles.

Use purpose-built test doubles for external boundaries rather than general-purpose mocking libraries. Create dedicated helpers for each boundary type: HTTP clients, sessions, filesystem, environment variables, databases. These helpers encapsulate the boundary's behavior and provide a cleaner testing interface than ad-hoc mocks.

### [MR4] Mocking indicates design problems.

If your tests need to patch application code, refactor the design. Extract units (pure functions) and integrators (assemblers) so they are directly testable. Move side effects to explicit boundary adapters invoked by actions. Represent outcomes with result types instead of exceptions to simplify testing.
