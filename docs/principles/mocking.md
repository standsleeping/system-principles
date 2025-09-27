# Mocking

This document defines concrete principles and usage patterns for mocking external boundaries in tests. It is grounded in the centralized boundary helpers provided by `boundaries.py` and expands on the high‑level rules in `projects.md` with practical code examples.

## Principles

### [MR1] Never mock application code.

Do not patch or fake your own functions, units, or integrators. Instead, run real code paths and only mock external boundaries.

```python
# BAD: Patching application internals
from unittest.mock import patch

from myapp.orders import process_order


def test_process_order_uses_patch():
    with patch("myapp.utils.calculate_total", return_value=42):
        result = process_order(order_id="O-123")
        assert result.is_ok
```

```python
# GOOD: Mock only external boundary (HTTP) and run real app code
from boundaries import mock_http, MockHttpResponse
from myapp.orders import process_order


def test_process_order_real_code_boundary_mock():
    with mock_http() as http:
        http.mock_post(
            "https://payments.example.com/charge",
            MockHttpResponse(status_code=200, json_data={"ok": True, "id": "ch_1"}),
        )
        result = process_order(order_id="O-123")
        assert result.is_ok
```

### [MR2] Mock only external boundaries.

Use the helpers in `boundaries.py` to simulate HTTP, filesystem, environment, and session state. Keep your domain logic real.

```python
# Filesystem boundary example
from pathlib import Path
from boundaries import mock_filesystem, MockFileSystem, MockFile


def test_reads_file_from_fs_boundary():
    structure = MockFileSystem(
        files=[MockFile(path=Path("inputs/data.txt"), content="hello world")]
    )

    with mock_filesystem(structure) as fs_dir:
        data_path = fs_dir / "inputs" / "data.txt"
        assert data_path.read_text() == "hello world"
```

```python
# Environment boundary example
import os
from boundaries import mock_env


def test_env_vars_boundary():
    with mock_env({"APP_MODE": "test"}, clear_prefix="APP_"):
        assert os.environ["APP_MODE"] == "test"
    # Environment restored afterwards
```

```python
# Session boundary example
from boundaries import mock_session


def test_session_boundary():
    with mock_session({"user_id": "u_123"}) as session:
        assert session["user_id"] == "u_123"
```

### [MR3] No unittest.mock in tests.

Do not import `unittest.mock` directly in test suites. Use the boundary helpers that encapsulate mocking.

```python
# DO NOT DO THIS
from unittest.mock import patch

# ... test code that patches application or third-party calls ...
```

```python
# DO THIS: use boundary helpers instead
from boundaries import mock_http, MockHttpResponse


def test_fetch_profile_uses_http_boundary():
    with mock_http() as http:
        http.mock_get(
            "https://api.example.com/profile/u_123",
            MockHttpResponse(json_data={"id": "u_123", "name": "Ada"}),
        )
        # call real code that performs the HTTP GET
        profile = fetch_profile("u_123")
        assert profile.name == "Ada"
```

### [MR4] Use boundary mockers for endpoints and translators.

- For HTTP endpoints: use `TestClient` plus `mock_http()` to simulate upstream calls.
- For translators (request parsing): use `mock_request()` to create real `starlette.requests.Request` objects without a server.

```python
# Endpoint example with TestClient + mock_http
from starlette.testclient import TestClient
from boundaries import mock_http, MockHttpResponse


def test_get_orders_endpoint(app):
    client = TestClient(app)

    with mock_http() as http:
        http.mock_get(
            "https://orders.example.com/api/orders?user_id=u_123",
            MockHttpResponse(json_data={"orders": [{"id": "O-1"}]}),
        )
        res = client.get("/api/orders?user_id=u_123")
        assert res.status_code == 200
        assert res.json()["orders"][0]["id"] == "O-1"
```

```python
# Translator example with mock_request
from boundaries import mock_request

# Example sync translator that expects already-parsed payload
# (In async contexts, prefer `await request.json()` and make the
# translator async or parse body before calling the translator.)

def translate_create_user_request(request):
    # If using `mock_request(json_data=...)`, the body is JSON-encoded.
    # Here we assume the caller provided parsed payload for this example.
    # Adapt as needed for your translator’s contract.
    payload = {"name": "Ana"}
    return {"name": payload.get("name")}


def test_translator_with_real_request_object():
    req = mock_request(json_data={"name": "Ana"}, path="/users", method="POST")
    result = translate_create_user_request(req)
    assert result == {"name": "Ana"}
```

### [MR5] Mocking indicates design problems.

If your tests "need" to patch application code, refactor the design:
- Extract units (pure functions) and integrators (assemblers) so they are directly testable.
- Move side effects to explicit boundary adapters invoked by actions.
- Represent outcomes with result types instead of exceptions to simplify testing.

```python
# BEFORE (hard to test, tends to require patching)
# def checkout(user_id):
#     total = calculate_total(fetch_cart(user_id))
#     charge_card(total)  # directly performs HTTP call
#     return True

# AFTER (separated boundary makes testing easy)
# def checkout(user_id, charge):  # charge is a boundary adapter function
#     total = calculate_total(fetch_cart(user_id))
#     ok = charge(total)  # injected boundary adapter is mocked by mock_http()
#     return ok
```

## Boundary Mocking API (from `boundaries.py`)

Quick examples for the provided helpers.

```python
# HTTP
from boundaries import mock_http, MockHttpResponse

with mock_http() as http:
    http.mock_get("https://svc/x", MockHttpResponse(json_data={"ok": True}))
    http.mock_post("https://svc/y", MockHttpResponse(status_code=201))
    http.mock_any("https://svc/any", MockHttpResponse(text_data="pong"))
```

```python
# Filesystem
from pathlib import Path
from boundaries import mock_filesystem, MockFileSystem, MockFile

structure = MockFileSystem(
    files=[MockFile(path=Path("a/b.txt"), content="hi")],
    directories=[Path("c/d")],
)

with mock_filesystem(structure) as fs:
    assert (fs / "a/b.txt").read_text() == "hi"
```

```python
# Environment
from boundaries import mock_env

with mock_env({"FEATURE_X": "1"}, clear_prefix="FEATURE_"):
    # env within context is modified; restored after
    pass
```

```python
# Session
from boundaries import mock_session

with mock_session({"user_id": "u_1"}) as session:
    assert session["user_id"] == "u_1"
```

```python
# Combined boundaries
from boundaries import (
    mock_boundaries,
    MockHttpResponse,
    MockFileSystem,
    MockFile,
)
from pathlib import Path

http_mocks = {
    "https://svc/ping": MockHttpResponse(json_data={"pong": True}),
}
fs = MockFileSystem(files=[MockFile(Path("input.txt"), content="data")])

auth_token = "testtoken"

def test_with_all_boundaries():
    with mock_boundaries(
        http_mocks=http_mocks,
        filesystem=fs,
        env_vars={"AUTH_TOKEN": auth_token},
        clear_env_prefix="AUTH_",
        session_data={"user": "u_1"},
    ) as (http, fs_dir, session):
        # use http, fs_dir, session inside the test
        pass
```

## Guidance

- Keep boundary mocks narrow and explicit; prefer `MockHttpResponse` for clarity.
- Avoid over-specifying behavior. Assert on inputs/outputs of your functions, not internal calls.
- Prefer translator testing with `mock_request()` for parsing and validation boundaries.
- Never patch domain code; refactor toward actions/integrators/units.

