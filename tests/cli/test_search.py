"""Integration tests for `principles search`."""

import tempfile
from pathlib import Path

from principles.main import main


def _write_principle(
    content_dir: Path,
    pid: str,
    title: str = "Title",
    essence: str = "Essence text.",
    body: str = "Body content.",
    tags: list[str] | None = None,
) -> None:
    tags_line = f"\ntags: {tags}" if tags else ""
    text = f"""---
id: {pid}
title: "{title}"
essence: "{essence}"{tags_line}
---

{body}
"""
    (content_dir / f"{pid.lower()}.md").write_text(text)


def test_search_finds_match(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        content = Path(tmpdir) / "content"
        content.mkdir()
        _write_principle(content, "FOO", title="Dispatch tables")
        _write_principle(content, "BAR", title="Unrelated")

        exit_code = main(["--content-dir", str(content), "search", "dispatch"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "FOO" in captured.out
        assert "BAR" not in captured.out


def test_search_no_matches(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        content = Path(tmpdir) / "content"
        content.mkdir()
        _write_principle(content, "FOO", title="Anything")

        exit_code = main(["--content-dir", str(content), "search", "ghost"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "No matches" in captured.out


def test_search_field_restriction(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        content = Path(tmpdir) / "content"
        content.mkdir()
        _write_principle(content, "FOO", title="Anything", body="Mentions dispatch.")

        exit_code = main([
            "--content-dir", str(content),
            "search", "dispatch", "--field", "title",
        ])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "No matches" in captured.out


def test_search_limit(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        content = Path(tmpdir) / "content"
        content.mkdir()
        for i in range(5):
            _write_principle(content, f"P{i}", title=f"Pattern {i}")

        exit_code = main([
            "--content-dir", str(content),
            "search", "Pattern", "--limit", "2",
        ])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "more — pass --limit" in captured.out
