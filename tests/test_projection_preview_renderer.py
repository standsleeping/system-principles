"""Checks for the projection matrix preview renderer."""

import importlib.util
import json
from pathlib import Path

RENDERER_PATH = (
    Path(__file__).resolve().parents[1]
    / "config/claude/skills/concept-artifacts/scripts/render_projection_preview.py"
)
SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "config/claude/skills/concept-artifacts/schemas/projection-matrix.schema.json"
)

spec = importlib.util.spec_from_file_location("projection_preview", RENDERER_PATH)
assert spec is not None
assert spec.loader is not None
projection_preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection_preview)


def _write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _matrix() -> dict[str, object]:
    return {
        "$schema": "projection-matrix.schema.json",
        "concept": "Task",
        "generated_from": {
            "definition": "concepts/task.json",
            "manifest": "concepts/surfaces/task.json",
            "channels": "concepts/channels.json",
        },
        "channels": [
            {
                "key": "web-ui",
                "direction": "bi",
                "sync": "sync",
                "transport": "HTTP",
                "encoding": "HTML",
                "surface": "visual-controls",
            },
            {
                "key": "cli",
                "direction": "caller->system",
                "sync": "sync",
                "transport": "local",
                "encoding": "plaintext",
                "surface": "command",
            },
        ],
        "actions": [
            {
                "name": "create",
                "cells": [
                    {
                        "channel": "web-ui",
                        "status": "projected",
                        "element": "button",
                        "label": "Create task",
                        "source": "concepts/surfaces/task.json",
                    },
                    {
                        "channel": "cli",
                        "status": "excluded",
                        "reason": "CLI projection is intentionally absent.",
                        "source": "concepts/surfaces/task.json",
                    },
                ],
            }
        ],
        "emissions": [
            {
                "name": "task.created",
                "cells": [
                    {
                        "channel": "web-ui",
                        "status": "missing",
                        "expected_from": "concepts/surfaces/task.json",
                    },
                    {
                        "channel": "cli",
                        "status": "not-applicable",
                        "reason": "Channel direction is caller->system only.",
                    },
                ],
            }
        ],
    }


def test_load_projection_matrices_from_concepts_dir(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "concepts"
    _write_json(concepts_dir / "projection-matrices/task.json", _matrix())

    matrices = projection_preview.load_projection_matrices(concepts_dir)

    assert [matrix["concept"] for matrix in matrices] == ["Task"]


def test_render_preview_html_includes_summary_and_statuses() -> None:
    html = projection_preview.render_preview_html([_matrix()])

    assert "Projection Matrix Preview" in html
    assert "Task" in html
    assert "status-projected" in html
    assert "status-excluded" in html
    assert "status-missing" in html
    assert "status-not_applicable" in html
    assert "<strong>1</strong>" in html
    assert "button: Create task" in html


def test_write_projection_preview(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "concepts"
    output_path = tmp_path / "preview.html"
    _write_json(concepts_dir / "projection-matrices/task.json", _matrix())

    written = projection_preview.write_projection_preview(concepts_dir, output_path)

    assert written == output_path
    assert output_path.exists()
    assert "task.created" in output_path.read_text()


def _note_matrix() -> dict[str, object]:
    return {
        "$schema": "projection-matrix.schema.json",
        "concept": "Note",
        "generated_from": {
            "definition": "concepts/note.json",
            "manifest": "concepts/surfaces/note.json",
        },
        "channels": [
            {"key": "web-ui", "direction": "bi"},
        ],
        "actions": [
            {
                "name": "archive",
                "cells": [
                    {
                        "channel": "web-ui",
                        "status": "projected",
                        "element": "button",
                        "label": "Archive note",
                        "source": "concepts/surfaces/note.json",
                    },
                ],
            }
        ],
        "emissions": [],
    }


def test_render_multiple_matrices_aggregates_counts_and_concepts(
    tmp_path: Path,
) -> None:
    matrix_dir = tmp_path / "concepts/projection-matrices"
    _write_json(matrix_dir / "task.json", _matrix())
    _write_json(matrix_dir / "note.json", _note_matrix())

    matrices = projection_preview.load_projection_matrices(matrix_dir)
    counts = projection_preview.status_counts(matrices)
    html = projection_preview.render_preview_html(matrices)

    assert [matrix["concept"] for matrix in matrices] == ["Note", "Task"]
    assert projection_preview.row_count(matrices, "actions") == 2
    assert projection_preview.row_count(matrices, "emissions") == 1
    assert counts["projected"] == 2
    assert counts["excluded"] == 1
    assert counts["missing"] == 1
    assert counts["not-applicable"] == 1
    assert "Note" in html
    assert "Task" in html


def test_renderer_handles_every_schema_cell_status() -> None:
    schema = json.loads(SCHEMA_PATH.read_text())
    statuses = schema["$defs"]["projection_cell"]["properties"]["status"]["enum"]
    sample_fields: dict[str, dict[str, object]] = {
        "projected": {"element": "button", "label": "Do it", "source": "s.json"},
        "excluded": {"reason": "intentionally absent", "source": "s.json"},
        "missing": {"expected_from": "s.json"},
        "not-applicable": {"reason": "Channel direction is caller->system only."},
    }

    assert set(projection_preview.STATUSES) == set(statuses)
    for status in statuses:
        cell = {"channel": "web-ui", "status": status, **sample_fields[status]}
        text = projection_preview.cell_text(cell)
        assert text and text != status
