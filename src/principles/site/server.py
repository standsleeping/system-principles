"""Minimal development server for the static site."""

import functools
import http.server
from pathlib import Path

from principles.logging import get_logger

logger = get_logger(__name__)


def serve_site(directory: Path, port: int) -> None:
    """Serve the static site on localhost."""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(directory),
    )
    with http.server.HTTPServer(("localhost", port), handler) as server:
        print(f"Serving site at http://localhost:{port}/ (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
