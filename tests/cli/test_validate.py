"""Integration tests for `principles validate`."""

import tempfile
from pathlib import Path

from principles.main import main


def _write_principle(content_dir: Path, pid: str, related: list[str] | None = None) -> None:
    related_line = f"\nrelated: {related}" if related else ""
    body = f"""---
id: {pid}
title: "{pid} title"
essence: "essence"{related_line}
---

Body.
"""
    (content_dir / f"{pid.lower()}.md").write_text(body)


def test_validate_passes_on_clean_repo(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        content = root / "content"
        content.mkdir()
        _write_principle(content, "FOO", related=["BAR"])
        _write_principle(content, "BAR")

        exit_code = main([
            "--content-dir", str(content),
            "--taxonomies-dir", str(root / "taxonomies"),
            "--sets-dir", str(root / "sets"),
            "validate",
        ])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "All checks passed" in captured.out


def test_validate_flags_unknown_related(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        content = root / "content"
        content.mkdir()
        _write_principle(content, "FOO", related=["GHOST"])

        exit_code = main([
            "--content-dir", str(content),
            "--taxonomies-dir", str(root / "taxonomies"),
            "--sets-dir", str(root / "sets"),
            "validate",
        ])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "GHOST" in captured.out
        assert "Related references" in captured.out


def test_validate_flags_filename_mismatch(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        content = root / "content"
        content.mkdir()
        (content / "wrong_name.md").write_text("""---
id: FOO_BAR
title: "FOO_BAR title"
essence: "essence"
---

Body.
""")

        exit_code = main([
            "--content-dir", str(content),
            "--taxonomies-dir", str(root / "taxonomies"),
            "--sets-dir", str(root / "sets"),
            "validate",
        ])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "wrong_name.md" in captured.out
        assert "Filename consistency" in captured.out


def test_validate_flags_broken_set_reference(capsys) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        content = root / "content"
        content.mkdir()
        _write_principle(content, "FOO")

        sets_dir = root / "sets"
        sets_dir.mkdir()
        (sets_dir / "core.yaml").write_text("""name: core
description: ""
principles:
  - GHOST
""")

        exit_code = main([
            "--content-dir", str(content),
            "--taxonomies-dir", str(root / "taxonomies"),
            "--sets-dir", str(sets_dir),
            "validate",
        ])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "GHOST" in captured.out
        assert "Set references" in captured.out
