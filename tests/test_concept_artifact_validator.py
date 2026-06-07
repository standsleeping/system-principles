"""Tests for the concept artifact validator script."""

import importlib.util
import json
from pathlib import Path

from jsonschema import validate

VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1]
    / "config/claude/skills/concept-artifacts/scripts/validate_concepts.py"
)
SCHEMAS_PATH = (
    Path(__file__).resolve().parents[1]
    / "config/claude/skills/concept-artifacts/schemas"
)

spec = importlib.util.spec_from_file_location("concept_validator", VALIDATOR_PATH)
assert spec is not None
assert spec.loader is not None
concept_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(concept_validator)


def _write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data))


def _make_concepts_dir(
    tmp_path: Path,
    manifest: dict[str, object],
    concept_overrides: dict[str, object] | None = None,
) -> Path:
    concepts_dir = tmp_path / "concepts"
    surfaces_dir = concepts_dir / "surfaces"
    surfaces_dir.mkdir(parents=True)

    _write_json(
        concepts_dir / "dependency-graph.json",
        {
            "concepts": ["Task"],
            "specs": [],
            "dependencies": [],
        },
    )
    _write_json(
        concepts_dir / "coherence.json",
        {
            "concepts": ["Task"],
        },
    )
    _write_json(
        concepts_dir / "channels.json",
        {
            "$schema": "channel-registry.schema.json",
            "channels": [
                {
                    "key": "web-ui",
                    "transport": "HTTP",
                    "encoding": "HTML",
                    "surface": "button",
                    "direction": "bi",
                    "sync": "sync",
                    "auth_model": "session",
                },
                {
                    "key": "cli",
                    "transport": "local",
                    "encoding": "plaintext",
                    "surface": "command",
                    "direction": "caller->system",
                    "sync": "sync",
                    "auth_model": "local",
                },
            ],
        },
    )
    concept: dict[str, object] = {
        "$schema": "concept-definition.schema.json",
        "seed": {"kind": "concept", "name": "Task"},
        "actions": [{"name": "create"}],
        "state": [{"name": "tasks"}],
    }
    if concept_overrides:
        concept.update(concept_overrides)
    _write_json(concepts_dir / "task.json", concept)
    _write_json(surfaces_dir / "task.json", manifest)

    return concepts_dir


def _manifest(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "$schema": "concept-manifest.schema.json",
        "concept": "Task",
        "target_channels": ["web-ui", "cli"],
        "surfaces": [
            {
                "channel": "web-ui",
                "actions": [
                    {
                        "action": "create",
                        "element": "button",
                        "label": "Create task",
                    }
                ],
                "state": [
                    {
                        "component": "tasks",
                        "element": "task list",
                        "visibility": "always",
                    }
                ],
                "op_hint": "The create button appends a task to the list.",
            }
        ],
        "gaps": [],
    }
    data.update(overrides)
    return data


def test_target_channels_require_surface_or_channel_exclusion(
    tmp_path: Path,
    capsys,
) -> None:
    concepts_dir = _make_concepts_dir(tmp_path, _manifest())

    failures = concept_validator.level_2_cross_artifact(concepts_dir, SCHEMAS_PATH)

    captured = capsys.readouterr()
    assert failures == 1
    assert "Target channels have surfaces or channel exclusions" in captured.out
    assert "Task:cli" in captured.out


def test_channel_exclusion_satisfies_target_channel_coverage(
    tmp_path: Path,
    capsys,
) -> None:
    concepts_dir = _make_concepts_dir(
        tmp_path,
        _manifest(
            channel_exclusions=[
                {
                    "channel": "cli",
                    "reason": "Task creation is intentionally web-only here.",
                }
            ],
        ),
    )

    failures = concept_validator.level_2_cross_artifact(concepts_dir, SCHEMAS_PATH)

    captured = capsys.readouterr()
    assert failures == 0
    assert "Target channels have surfaces or channel exclusions" in captured.out


def test_emission_projection_references_real_emission(
    tmp_path: Path,
    capsys,
) -> None:
    manifest = _manifest(
        channel_exclusions=[
            {
                "channel": "cli",
                "reason": "CLI has no outbound delivery surface in this fixture.",
            }
        ],
    )
    surface = manifest["surfaces"][0]
    assert isinstance(surface, dict)
    surface["emissions"] = [
        {
            "emission": "created",
            "element": "toast",
            "label": "Task created",
        }
    ]
    concepts_dir = _make_concepts_dir(
        tmp_path,
        manifest,
        concept_overrides={
            "emissions": [
                {
                    "name": "created",
                    "trigger": "Task is created.",
                    "payload": "TaskCreated",
                    "delivery": "best-effort UI notification",
                }
            ]
        },
    )

    failures = concept_validator.level_2_cross_artifact(concepts_dir, SCHEMAS_PATH)

    captured = capsys.readouterr()
    assert failures == 0
    assert "Surface emission projections reference real emissions" in captured.out
    assert "Emission coverage" in captured.out


def test_emissions_require_projection_or_exclusion_on_outbound_channels(
    tmp_path: Path,
    capsys,
) -> None:
    concepts_dir = _make_concepts_dir(
        tmp_path,
        _manifest(
            channel_exclusions=[
                {
                    "channel": "cli",
                    "reason": "CLI has no outbound delivery surface in this fixture.",
                }
            ],
        ),
        concept_overrides={
            "emissions": [
                {
                    "name": "created",
                    "trigger": "Task is created.",
                    "payload": "TaskCreated",
                    "delivery": "best-effort UI notification",
                }
            ]
        },
    )

    failures = concept_validator.level_2_cross_artifact(concepts_dir, SCHEMAS_PATH)

    captured = capsys.readouterr()
    assert failures == 1
    assert "Emission coverage" in captured.out
    assert "Task:web-ui:created" in captured.out


def test_emission_projection_rejects_inbound_only_channel(
    tmp_path: Path,
    capsys,
) -> None:
    manifest = _manifest(
        target_channels=["cli"],
        surfaces=[
            {
                "channel": "cli",
                "actions": [
                    {
                        "action": "create",
                        "element": "command",
                        "label": "task create",
                    }
                ],
                "emissions": [
                    {
                        "emission": "created",
                        "element": "stdout-event",
                        "label": "Task created",
                    }
                ],
                "state": [
                    {
                        "component": "tasks",
                        "element": "task list output",
                        "visibility": "on-demand",
                    }
                ],
                "op_hint": "The command creates a task.",
            }
        ],
    )
    concepts_dir = _make_concepts_dir(
        tmp_path,
        manifest,
        concept_overrides={
            "emissions": [
                {
                    "name": "created",
                    "trigger": "Task is created.",
                    "payload": "TaskCreated",
                    "delivery": "best-effort UI notification",
                }
            ]
        },
    )

    failures = concept_validator.level_2_cross_artifact(concepts_dir, SCHEMAS_PATH)

    captured = capsys.readouterr()
    assert failures == 1
    assert "Emission projections use outbound-capable channels" in captured.out
    assert "Task:cli:created" in captured.out


def test_projection_matrix_generator_derives_statuses_and_valid_schema(
    tmp_path: Path,
) -> None:
    manifest = _manifest(
        target_channels=["web-ui", "cli", "webhook"],
        surfaces=[
            {
                "channel": "web-ui",
                "actions": [
                    {
                        "action": "create",
                        "element": "button",
                        "label": "Create task",
                    }
                ],
                "emissions": [
                    {
                        "emission": "created",
                        "element": "toast",
                        "label": "Task created",
                    }
                ],
                "state": [
                    {
                        "component": "tasks",
                        "element": "task list",
                        "visibility": "always",
                    }
                ],
                "op_hint": "The create button appends a task to the list.",
            },
            {
                "channel": "cli",
                "actions": [
                    {
                        "action": "create",
                        "element": "command",
                        "label": "task create",
                    }
                ],
                "state": [],
                "op_hint": "The command appends a task.",
            },
            {
                "channel": "webhook",
                "actions": [],
                "exclusions": [
                    {
                        "action": "create",
                        "reason": "Webhook is outbound-only.",
                    }
                ],
                "state": [],
                "op_hint": "The webhook can notify integrations later.",
            },
        ],
    )
    concepts_dir = _make_concepts_dir(
        tmp_path,
        manifest,
        concept_overrides={
            "emissions": [
                {
                    "name": "created",
                    "trigger": "Task is created.",
                    "payload": "TaskCreated",
                    "delivery": "best-effort UI notification",
                }
            ]
        },
    )
    channels = concept_validator.load_json(concepts_dir / "channels.json")
    channels["channels"].append(
        {
            "key": "webhook",
            "transport": "HTTP",
            "encoding": "JSON",
            "surface": "callback-url",
            "direction": "system->caller",
            "sync": "async",
            "auth_model": "shared-secret",
        }
    )
    _write_json(concepts_dir / "channels.json", channels)

    matrix = concept_validator.generate_projection_matrix(
        concepts_dir,
        concepts_dir / "task.json",
        concepts_dir / "surfaces/task.json",
        concepts_dir / "channels.json",
    )
    schema = concept_validator.load_json(SCHEMAS_PATH / "projection-matrix.schema.json")
    validate(matrix, schema)

    action_row = matrix["actions"][0]
    assert isinstance(action_row, dict)
    action_cells = {
        cell["channel"]: cell["status"] for cell in action_row["cells"]
    }
    assert action_cells == {
        "web-ui": "projected",
        "cli": "projected",
        "webhook": "excluded",
    }

    emission_row = matrix["emissions"][0]
    assert isinstance(emission_row, dict)
    emission_cells = {
        cell["channel"]: cell["status"] for cell in emission_row["cells"]
    }
    assert emission_cells == {
        "web-ui": "projected",
        "cli": "not-applicable",
        "webhook": "missing",
    }


def test_projection_matrix_missing_cells_fail_level_2(
    tmp_path: Path,
    capsys,
) -> None:
    concepts_dir = _make_concepts_dir(
        tmp_path,
        _manifest(
            channel_exclusions=[
                {
                    "channel": "cli",
                    "reason": "Task creation is intentionally web-only here.",
                }
            ],
        ),
    )
    matrices_dir = concepts_dir / "projection-matrices"
    matrices_dir.mkdir()
    _write_json(
        matrices_dir / "task.json",
        {
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
                }
            ],
            "actions": [
                {
                    "name": "create",
                    "cells": [
                        {
                            "channel": "web-ui",
                            "status": "missing",
                            "expected_from": "concepts/surfaces/task.json",
                        }
                    ],
                }
            ],
            "emissions": [],
        },
    )

    failures = concept_validator.level_2_cross_artifact(concepts_dir, SCHEMAS_PATH)

    captured = capsys.readouterr()
    assert failures == 1
    assert "Projection matrix coverage: no missing cells" in captured.out
    assert "Task:action:web-ui:create" in captured.out
