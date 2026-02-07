"""Tests for the main function."""

import tempfile
from pathlib import Path

from principles.main import main


def test_main_no_command_shows_help(capsys) -> None:
    """Shows help when no command given."""
    # main() with no args calls parse_args(["--help"]) which exits
    # We just verify it doesn't crash
    exit_code = main([])
    assert exit_code == 0


def test_main_list_empty_content(capsys) -> None:
    """List command with no content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code = main(["--content-dir", tmpdir, "list"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "No principles found" in captured.out


def test_main_list_with_content(capsys) -> None:
    """List command with content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a sample principle
        content_dir = Path(tmpdir) / "content" / "designing" / "boundaries"
        content_dir.mkdir(parents=True)
        (content_dir / "BD1.md").write_text(
            """---
id: BD1
title: Test Principle
essence: A test principle
---

Content here.
"""
        )

        exit_code = main(["--content-dir", str(Path(tmpdir) / "content"), "list"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "BD1" in captured.out
        assert "Test Principle" in captured.out
