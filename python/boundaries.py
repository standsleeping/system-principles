"""
Centralized module for mocking all boundary-level interactions in tests.

This module provides a unified interface for mocking:
- HTTP requests and responses
- HTTP Session data
- File system operations
- Environment variables
- Other external system boundaries
"""

import os
import json
from pathlib import Path
from typing import Any, Protocol
from tempfile import TemporaryDirectory
from contextlib import contextmanager
from dataclasses import dataclass, field
from urllib.parse import urlencode

import respx
from httpx import Response
from starlette.requests import Request


# ==============================================================================
# HTTP
# ==============================================================================


@dataclass
class MockHttpResponse:
    """Represents a mocked HTTP response."""

    status_code: int = 200
    json_data: dict[str, Any] | None = None
    text_data: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    content_type: str | None = None

    def to_httpx_response(self) -> Response:
        """Convert to httpx Response object."""
        headers = self.headers.copy()

        if self.content_type:
            headers["content-type"] = self.content_type

        if self.json_data is not None:
            headers.setdefault("content-type", "application/json")
            return Response(self.status_code, json=self.json_data, headers=headers)
        elif self.text_data is not None:
            return Response(self.status_code, text=self.text_data, headers=headers)
        else:
            return Response(self.status_code, headers=headers)


class MockState:
    """Mock request state object for adding state attributes."""

    def __init__(self, data: dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)


def mock_request(
    form_data: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None,
    query_params: dict[str, str] | None = None,
    session_data: dict[str, Any] | None = None,
    state: dict[str, Any] | None = None,
    path: str = "/",
    method: str = "POST",
) -> Request:
    """
    Create a real Starlette Request object for testing TRANSLATOR functions.

    Args:
        form_data: Dictionary of form field data (for web APIs)
        json_data: Dictionary of JSON data (for JSON APIs)
        query_params: Dictionary of query parameters
        session_data: Dictionary of session data
        state: Dictionary of request state data
        path: Request path
        method: HTTP method

    Returns:
        Real Starlette Request object
    """
    # Determine content type and body based on data provided
    if json_data is not None:
        # JSON request
        body = json.dumps(json_data).encode("utf-8")
        content_type = b"application/json"
    elif form_data is not None:
        # Form request
        body = urlencode(form_data).encode("utf-8")
        content_type = b"application/x-www-form-urlencoded"
    else:
        # Empty request
        body = b""
        content_type = b"text/plain"

    # Handle query parameters
    query_string = b""
    if query_params:
        query_string = urlencode(query_params).encode("utf-8")

    # Create ASGI scope
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "query_string": query_string,
        "headers": [
            (b"content-type", content_type),
            (b"content-length", str(len(body)).encode()),
        ],
    }

    # Create receive function that provides the request body
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    # Create the request
    request = Request(scope, receive)

    # Add session data if provided
    if session_data:
        request._session = session_data  # type: ignore

    # Add state data if provided
    if state:
        # Set state attributes individually to avoid assignment warning
        for key, value in state.items():
            setattr(request.state, key, value)

    return request


class HttpMocker(Protocol):
    """Protocol for HTTP mocking operations."""

    def mock_get(self, url: str, response: MockHttpResponse) -> None:
        """Mock a GET request."""
        ...

    def mock_post(self, url: str, response: MockHttpResponse) -> None:
        """Mock a POST request."""
        ...

    def mock_any(self, url: str, response: MockHttpResponse) -> None:
        """Mock any HTTP method."""
        ...


@contextmanager
def mock_http():
    """Context manager for mocking HTTP requests."""

    class HttpMockerImpl:
        def __init__(self, respx_mock):
            self.respx_mock = respx_mock

        def mock_get(self, url: str, response: MockHttpResponse) -> None:
            self.respx_mock.get(url).mock(return_value=response.to_httpx_response())

        def mock_post(self, url: str, response: MockHttpResponse) -> None:
            self.respx_mock.post(url).mock(return_value=response.to_httpx_response())

        def mock_any(self, url: str, response: MockHttpResponse) -> None:
            self.respx_mock.route(url=url).mock(
                return_value=response.to_httpx_response()
            )

    with respx.mock(assert_all_called=False) as respx_mock:
        yield HttpMockerImpl(respx_mock)


# ==============================================================================
# File System
# ==============================================================================


@dataclass
class MockFile:
    """Represents a mocked file."""

    path: Path
    content: str | bytes | dict | list
    is_json: bool = False

    def write(self, parent_dir: Path) -> Path:
        """Write the file to the given parent directory."""
        full_path = parent_dir / self.path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if self.is_json and isinstance(self.content, (dict, list)):
            with open(full_path, "w") as f:
                json.dump(self.content, f)
        elif isinstance(self.content, bytes):
            with open(full_path, "wb") as f:
                f.write(self.content)
        else:
            with open(full_path, "w") as f:
                f.write(self.content)

        return full_path


@dataclass
class MockFileSystem:
    """Represents a mocked file system structure."""

    files: list[MockFile] = field(default_factory=list)
    directories: list[Path] = field(default_factory=list)

    def create_in(self, parent_dir: Path) -> None:
        """Create the file system structure in the given directory."""
        # Create directories
        for directory in self.directories:
            full_path = parent_dir / directory
            full_path.mkdir(parents=True, exist_ok=True)

        # Create files
        for file in self.files:
            file.write(parent_dir)


@contextmanager
def mock_filesystem(structure: MockFileSystem | None = None):
    """Context manager for mocking file system operations."""
    with TemporaryDirectory() as temp_dir:  # type: ignore
        temp_path = Path(temp_dir)

        if structure:
            structure.create_in(temp_path)

        yield temp_path


# ==============================================================================
# Session Management
# ==============================================================================

from unittest.mock import patch


@contextmanager
def mock_session(session_data: dict[str, Any] | None = None):
    """
    Context manager for mocking Starlette session data.

    Args:
        session_data: Dictionary of session data to set
    """
    session = session_data or {}

    with patch("starlette.requests.Request.session", session):
        yield session


# ==============================================================================
# Environment Variables
# ==============================================================================


@contextmanager
def mock_env(
    variables: dict[str, str] | None = None,
    clear_prefix: str | None = None,
    path_prepend: list[str | Path] | None = None,
    path_append: list[str | Path] | None = None,
):
    """
    Context manager for mocking environment variables.

    Args:
        variables: Dictionary of environment variables to set
        clear_prefix: Clear all env vars starting with this prefix
        path_prepend: Paths to prepend to PATH (preserves existing PATH)
        path_append: Paths to append to PATH (preserves existing PATH)

    Examples:
        # Replace PATH entirely (fragile, may break system utilities)
        with mock_env({"PATH": "/custom/bin"}):
            subprocess.run(["my_tool"])

        # Prepend to PATH (preferred, preserves system utilities)
        with mock_env(path_prepend=["/custom/bin"]):
            subprocess.run(["my_tool"])

        # Combine with other env vars
        with mock_env({"DEBUG": "1"}, path_prepend=[lean_bin]):
            subprocess.run(["lake", "build"])
    """
    # Save current environment
    env_backup = os.environ.copy()

    try:
        # Clear variables with prefix if specified
        if clear_prefix:
            for key in list(os.environ.keys()):
                if key.startswith(clear_prefix):
                    del os.environ[key]

        # Set new variables
        if variables:
            for key, value in variables.items():
                os.environ[key] = value

        # Handle PATH modifications (after variables, so explicit PATH wins)
        if path_prepend or path_append:
            current_path = os.environ.get("PATH", "")
            path_parts = current_path.split(os.pathsep) if current_path else []

            if path_prepend:
                prepend_parts = [str(p) for p in path_prepend]
                path_parts = prepend_parts + path_parts

            if path_append:
                append_parts = [str(p) for p in path_append]
                path_parts = path_parts + append_parts

            os.environ["PATH"] = os.pathsep.join(path_parts)

        yield

    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(env_backup)


# ==============================================================================
# Subprocess
# ==============================================================================


@dataclass
class MockSubprocessResult:
    """Represents a mocked subprocess result."""

    returncode: int = 0
    stdout: str = ""
    stderr: str = ""


class SubprocessMocker:
    """
    Mocker for subprocess.run calls.

    Registers command patterns and returns mock results when matched.
    Commands are matched by prefix (the registered pattern must be a prefix
    of the actual command).
    """

    def __init__(self):
        self._mocks: list[tuple[list[str], MockSubprocessResult]] = []
        self._calls: list[list[str]] = []

    def mock_run(
        self,
        command: list[str],
        result: MockSubprocessResult,
    ) -> None:
        """
        Register a mock response for a command.

        Args:
            command: Command prefix to match (e.g., ["lake", "build"])
            result: MockSubprocessResult to return when matched
        """
        self._mocks.append((command, result))

    def _find_mock(self, command: list[str]) -> MockSubprocessResult | None:
        """Find a mock that matches the command prefix."""
        for pattern, result in self._mocks:
            if len(command) >= len(pattern) and command[: len(pattern)] == pattern:
                return result
        return None

    def _handle_call(self, command: list[str], **kwargs) -> MockSubprocessResult:
        """Handle a subprocess.run call."""
        self._calls.append(command)
        result = self._find_mock(command)
        if result is None:
            raise ValueError(
                f"No mock registered for command: {command}\n"
                f"Registered mocks: {[m[0] for m in self._mocks]}"
            )
        return result

    @property
    def calls(self) -> list[list[str]]:
        """Return list of commands that were called."""
        return self._calls.copy()

    def assert_called_with(self, command: list[str]) -> None:
        """Assert that a specific command was called."""
        if command not in self._calls:
            raise AssertionError(
                f"Command {command} was not called.\nActual calls: {self._calls}"
            )


@contextmanager
def mock_subprocess():
    """
    Context manager for mocking subprocess.run calls.

    Use this for unit tests where you want to avoid running real subprocesses.
    For integration tests that run real subprocesses, use mock_env with
    path_prepend instead.

    Example:
        with mock_subprocess() as proc:
            proc.mock_run(
                ["lake", "build"],
                MockSubprocessResult(returncode=0, stdout="Build successful"),
            )
            proc.mock_run(
                ["lake", "build", "--error"],
                MockSubprocessResult(returncode=1, stderr="Build failed"),
            )

            # Your code that calls subprocess.run(["lake", "build", ...])
            result = my_function_that_runs_subprocess()

            # Verify calls
            proc.assert_called_with(["lake", "build"])
    """
    import subprocess

    mocker = SubprocessMocker()
    original_run = subprocess.run

    def mock_run(args, **kwargs):
        cmd = list(args) if not isinstance(args, list) else args
        result = mocker._handle_call(cmd, **kwargs)

        # Create a CompletedProcess-like object
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=result.returncode,
            stdout=result.stdout if kwargs.get("capture_output") or kwargs.get("stdout") else None,
            stderr=result.stderr if kwargs.get("capture_output") or kwargs.get("stderr") else None,
        )

    with patch("subprocess.run", mock_run):
        yield mocker


@dataclass
class SubprocessInput:
    """
    Input configuration for subprocess execution with temporary files.

    Attributes:
        content: Content to write to the temporary file
        suffix: File extension (e.g., ".lean", ".py", ".txt")
        filename: Optional specific filename (otherwise auto-generated)
    """

    content: str
    suffix: str = ".txt"
    filename: str | None = None


class SubprocessError(Exception):
    """Raised when subprocess execution fails."""

    def __init__(self, message: str, result: "subprocess.CompletedProcess | None" = None):
        super().__init__(message)
        self.result = result


@contextmanager
def subprocess_with_tempfile(
    command_template: list[str],
    input_data: SubprocessInput,
    cwd: Path | None = None,
    env_path_prepend: list[str | Path] | None = None,
    timeout: int = 30,
):
    """
    Run subprocess with temporary input file and automatic cleanup.

    The command_template should contain "{input_file}" as a placeholder
    for the temporary file path.

    Args:
        command_template: Command with "{input_file}" placeholder
        input_data: SubprocessInput with content and file settings
        cwd: Working directory for the subprocess
        env_path_prepend: Paths to prepend to PATH for the subprocess
        timeout: Timeout in seconds

    Yields:
        subprocess.CompletedProcess result

    Example:
        input_data = SubprocessInput(
            content="import Mathport\\n#export_json x + 1",
            suffix=".lean",
        )

        with subprocess_with_tempfile(
            command_template=["lake", "env", "lean", "{input_file}"],
            input_data=input_data,
            cwd=mathport_path,
            env_path_prepend=[elan_bin],
        ) as result:
            if result.returncode == 0:
                output = json.loads(result.stdout)
    """
    import subprocess
    from tempfile import NamedTemporaryFile

    # Create temp file with appropriate suffix
    with NamedTemporaryFile(
        mode="w",
        suffix=input_data.suffix,
        delete=False,
    ) as tmp:
        tmp.write(input_data.content)
        tmp_path = Path(tmp.name)

    try:
        # Build command with temp file path
        command = [
            arg.replace("{input_file}", str(tmp_path)) if isinstance(arg, str) else arg
            for arg in command_template
        ]

        # Run with optional PATH modification
        with mock_env(path_prepend=env_path_prepend):
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

        yield result

    finally:
        # Clean up temp file
        tmp_path.unlink(missing_ok=True)


def parse_subprocess_json(
    result: "subprocess.CompletedProcess",
    line_index: int = 0,
) -> dict | list:
    """
    Parse JSON from subprocess stdout.

    Args:
        result: CompletedProcess from subprocess.run
        line_index: Which line of stdout to parse (default: first line)

    Returns:
        Parsed JSON as dict or list

    Raises:
        SubprocessError: If command failed or output is not valid JSON

    Example:
        result = subprocess.run(["my_tool", "--json"], capture_output=True, text=True)
        data = parse_subprocess_json(result)
    """
    if result.returncode != 0:
        raise SubprocessError(
            f"Command failed with return code {result.returncode}\n"
            f"stderr: {result.stderr}",
            result=result,
        )

    if not result.stdout:
        raise SubprocessError(
            "Command produced no output",
            result=result,
        )

    lines = result.stdout.strip().split("\n")
    if line_index >= len(lines):
        raise SubprocessError(
            f"Output has only {len(lines)} lines, cannot get line {line_index}\n"
            f"stdout: {result.stdout}",
            result=result,
        )

    try:
        return json.loads(lines[line_index])
    except json.JSONDecodeError as e:
        raise SubprocessError(
            f"Invalid JSON on line {line_index}: {e}\n"
            f"Content: {lines[line_index][:200]}...",
            result=result,
        ) from e


# ==============================================================================
# Combined Boundaries
# ==============================================================================


@contextmanager
def mock_boundaries(
    http_mocks: dict[str, MockHttpResponse] | None = None,
    filesystem: MockFileSystem | None = None,
    env_vars: dict[str, str] | None = None,
    clear_env_prefix: str | None = None,
    env_path_prepend: list[str | Path] | None = None,
    env_path_append: list[str | Path] | None = None,
    session_data: dict[str, Any] | None = None,
):
    """
    Comprehensive context manager for mocking all boundary interactions.

    Args:
        http_mocks: Dict of URL to MockHttpResponse mappings
        filesystem: MockFileSystem structure to create
        env_vars: Environment variables to set
        clear_env_prefix: Clear env vars with this prefix
        env_path_prepend: Paths to prepend to PATH
        env_path_append: Paths to append to PATH
        session_data: Session data to set

    Yields:
        tuple: (http_mocker, filesystem_path, session)
    """
    with mock_http() as http_mocker:
        # Set up HTTP mocks
        if http_mocks:
            for url, response in http_mocks.items():
                http_mocker.mock_any(url, response)

        with mock_filesystem(filesystem) as fs_path:
            with mock_env(
                env_vars,
                clear_env_prefix,
                path_prepend=env_path_prepend,
                path_append=env_path_append,
            ):
                with mock_session(session_data) as session:
                    yield http_mocker, fs_path, session
