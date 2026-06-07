"""Validate concept artifacts against schemas and cross-artifact consistency rules.

Usage: python validate_concepts.py <concepts_dir> <schemas_dir> [--level N ...]

Dependencies: jsonschema, referencing
"""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import ValidationError, validate
from referencing import Registry, Resource


def load_json(path: Path) -> dict[str, object]:
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def as_str(val: object) -> str:
    if not isinstance(val, str):
        raise TypeError(f"Expected str, got {type(val).__name__}")
    return val


def as_list(val: object) -> list[object]:
    if not isinstance(val, list):
        raise TypeError(f"Expected list, got {type(val).__name__}")
    return list(val)


def as_dict(val: object) -> dict[str, object]:
    if not isinstance(val, dict):
        raise TypeError(f"Expected dict, got {type(val).__name__}")
    return {str(k): v for k, v in val.items()}


OUTBOUND_DIRECTIONS = {"system->caller", "bi"}
INBOUND_ONLY_DIRECTION = "caller->system"


def is_outbound(direction: str | None) -> bool:
    """True when a channel can carry system->caller emissions."""
    return direction in OUTBOUND_DIRECTIONS


def build_schema_registry(schemas_dir: Path) -> Registry:
    """Build a referencing Registry from all schema files so $ref can resolve."""
    resources: list[tuple[str, Resource]] = []
    for schema_path in schemas_dir.glob("*.schema.json"):
        schema = load_json(schema_path)
        resource = Resource.from_contents(schema)
        resources.append((schema_path.name, resource))
    return Registry().with_resources(resources)


def iter_seeded_files(concepts_dir: Path) -> list[tuple[Path, dict[str, object]]]:
    """Walk concepts_dir and return every (path, data) where data has a `seed` key."""
    seeded: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(concepts_dir.rglob("*.json")):
        data = load_json(path)
        if "seed" in data:
            seeded.append((path, data))
    return seeded


def load_definitions(concepts_dir: Path, kind: str) -> dict[str, dict[str, object]]:
    """Load every definition whose seed.kind matches `kind`, indexed by seed.name."""
    definitions: dict[str, dict[str, object]] = {}
    for _path, data in iter_seeded_files(concepts_dir):
        seed = as_dict(data["seed"])
        if seed.get("kind") == kind:
            definitions[as_str(seed["name"])] = data
    return definitions


def discover_artifacts(concepts_dir: Path, schemas_dir: Path) -> dict[Path, Path]:
    """Map each concept file to its schema by reading the $schema field.

    Recursive: walks subdirectories (specs/, surfaces/, genericity/, ...) so
    every artifact is validated regardless of where it lives in the tree.
    """
    mapping: dict[Path, Path] = {}
    for path in sorted(concepts_dir.rglob("*.json")):
        data = load_json(path)
        schema_ref = data.get("$schema")
        if schema_ref is None:
            print_result(
                str(path.relative_to(concepts_dir)), False, "no $schema field, skipping"
            )
            continue
        schema_path = schemas_dir / as_str(schema_ref)
        if not schema_path.exists():
            print_result(
                str(path.relative_to(concepts_dir)),
                False,
                f"schema not found: {schema_ref}",
            )
            continue
        mapping[path] = schema_path
    return mapping


def print_result(label: str, passed: bool, detail: str = "") -> None:
    mark = "\u2713" if passed else "\u2717"
    msg = f"  {mark} {label}"
    if detail:
        msg += f" \u2014 {detail}"
    print(msg)


def artifact_source(path: Path, concepts_dir: Path) -> str:
    """Return a stable project-local source path for generated artifacts."""
    try:
        rel = path.relative_to(concepts_dir)
    except ValueError:
        return path.as_posix()
    return (Path(concepts_dir.name) / rel).as_posix()


def resolve_artifact_source(source: str, concepts_dir: Path) -> Path:
    """Resolve a generated_from source path back to a local artifact path."""
    source_path = Path(source)
    if source_path.is_absolute():
        return source_path
    if source_path.parts and source_path.parts[0] == concepts_dir.name:
        return concepts_dir.parent / source_path
    return concepts_dir / source_path


def load_definition_paths(concepts_dir: Path, kind: str) -> dict[str, Path]:
    """Load definition paths whose seed.kind matches `kind`, indexed by seed.name."""
    paths: dict[str, Path] = {}
    for path, data in iter_seeded_files(concepts_dir):
        seed = as_dict(data["seed"])
        if seed.get("kind") == kind:
            paths[as_str(seed["name"])] = path
    return paths


def ordered_channel_keys(manifest: dict[str, object]) -> list[str]:
    """Return matrix columns without adding any project-specific channel policy."""
    seen: set[str] = set()
    keys: list[str] = []

    def add(channel: str) -> None:
        if channel not in seen:
            seen.add(channel)
            keys.append(channel)

    surfaces = [as_dict(s) for s in as_list(manifest["surfaces"])]
    target_channels = [as_str(c) for c in as_list(manifest.get("target_channels", []))]
    channel_exclusions = [
        as_dict(e) for e in as_list(manifest.get("channel_exclusions", []))
    ]

    if target_channels:
        for channel in target_channels:
            add(channel)
    for surface in surfaces:
        add(as_str(surface["channel"]))
    for exclusion in channel_exclusions:
        add(as_str(exclusion["channel"]))

    return keys


def channel_registry_by_key(
    channels: dict[str, object] | None,
) -> dict[str, dict[str, object]]:
    if channels is None:
        return {}
    return {
        as_str(as_dict(channel)["key"]): as_dict(channel)
        for channel in as_list(channels["channels"])
    }


def matrix_channels(
    channel_keys: list[str],
    channels: dict[str, object] | None,
) -> list[dict[str, object]]:
    registry = channel_registry_by_key(channels)
    rendered: list[dict[str, object]] = []
    for key in channel_keys:
        registered = registry.get(key)
        if registered is None:
            rendered.append({"key": key, "direction": "unknown"})
            continue

        item: dict[str, object] = {"key": key}
        for field in (
            "direction",
            "sync",
            "transport",
            "encoding",
            "surface",
            "auth_model",
        ):
            if field in registered:
                item[field] = registered[field]
        rendered.append(item)
    return rendered


def generated_from_sources(
    concepts_dir: Path,
    definition_path: Path,
    manifest_path: Path,
    channels_path: Path | None,
) -> dict[str, object]:
    sources: dict[str, object] = {
        "definition": artifact_source(definition_path, concepts_dir),
        "manifest": artifact_source(manifest_path, concepts_dir),
    }
    if channels_path is not None:
        sources["channels"] = artifact_source(channels_path, concepts_dir)
    return sources


def surface_projection_maps(
    manifest: dict[str, object],
) -> tuple[
    dict[tuple[str, str], dict[str, object]],
    dict[tuple[str, str], dict[str, object]],
    dict[tuple[str, str], dict[str, object]],
    dict[tuple[str, str], dict[str, object]],
    dict[str, dict[str, object]],
]:
    action_projections: dict[tuple[str, str], dict[str, object]] = {}
    action_exclusions: dict[tuple[str, str], dict[str, object]] = {}
    emission_projections: dict[tuple[str, str], dict[str, object]] = {}
    emission_exclusions: dict[tuple[str, str], dict[str, object]] = {}
    channel_exclusions: dict[str, dict[str, object]] = {}

    for exclusion in as_list(manifest.get("channel_exclusions", [])):
        entry = as_dict(exclusion)
        channel_exclusions[as_str(entry["channel"])] = entry

    for surface in as_list(manifest["surfaces"]):
        surf = as_dict(surface)
        channel = as_str(surf["channel"])
        for projection in as_list(surf["actions"]):
            entry = as_dict(projection)
            action_projections[(channel, as_str(entry["action"]))] = entry
        for exclusion in as_list(surf.get("exclusions", [])):
            entry = as_dict(exclusion)
            action_exclusions[(channel, as_str(entry["action"]))] = entry
        for projection in as_list(surf.get("emissions", [])):
            entry = as_dict(projection)
            emission_projections[(channel, as_str(entry["emission"]))] = entry
        for exclusion in as_list(surf.get("emission_exclusions", [])):
            entry = as_dict(exclusion)
            emission_exclusions[(channel, as_str(entry["emission"]))] = entry

    return (
        action_projections,
        action_exclusions,
        emission_projections,
        emission_exclusions,
        channel_exclusions,
    )


def projected_cell(
    channel: str,
    projection: dict[str, object],
    source: str,
) -> dict[str, object]:
    return {
        "channel": channel,
        "status": "projected",
        "element": as_str(projection["element"]),
        "label": as_str(projection["label"]),
        "source": source,
    }


def excluded_cell(
    channel: str,
    exclusion: dict[str, object],
    source: str,
) -> dict[str, object]:
    return {
        "channel": channel,
        "status": "excluded",
        "reason": as_str(exclusion["reason"]),
        "source": source,
    }


def missing_cell(
    channel: str,
    expected_from: str,
) -> dict[str, object]:
    return {
        "channel": channel,
        "status": "missing",
        "expected_from": expected_from,
    }


def emission_not_applicable_cell(channel: str) -> dict[str, object]:
    return {
        "channel": channel,
        "status": "not-applicable",
        "reason": "Channel direction is caller->system only.",
    }


def generate_projection_matrix(
    concepts_dir: Path,
    definition_path: Path,
    manifest_path: Path,
    channels_path: Path | None = None,
) -> dict[str, object]:
    """Derive the dashboard projection matrix for one concept manifest."""
    definition = load_json(definition_path)
    manifest = load_json(manifest_path)
    channels = load_json(channels_path) if channels_path is not None else None

    concept = as_str(manifest["concept"])
    source = artifact_source(manifest_path, concepts_dir)
    channel_keys = ordered_channel_keys(manifest)
    registry = channel_registry_by_key(channels)

    (
        action_projections,
        action_exclusions,
        emission_projections,
        emission_exclusions,
        channel_exclusions,
    ) = surface_projection_maps(manifest)

    actions: list[dict[str, object]] = []
    for action_obj in as_list(definition.get("actions", [])):
        action = as_str(as_dict(action_obj)["name"])
        cells: list[dict[str, object]] = []
        for channel in channel_keys:
            projection = action_projections.get((channel, action))
            exclusion = action_exclusions.get((channel, action))
            channel_exclusion = channel_exclusions.get(channel)
            if projection is not None:
                cells.append(projected_cell(channel, projection, source))
            elif exclusion is not None:
                cells.append(excluded_cell(channel, exclusion, source))
            elif channel_exclusion is not None:
                cells.append(excluded_cell(channel, channel_exclusion, source))
            else:
                cells.append(missing_cell(channel, source))
        actions.append({"name": action, "cells": cells})

    emissions: list[dict[str, object]] = []
    for emission_obj in as_list(definition.get("emissions", [])):
        emission = as_str(as_dict(emission_obj)["name"])
        cells = []
        for channel in channel_keys:
            projection = emission_projections.get((channel, emission))
            exclusion = emission_exclusions.get((channel, emission))
            channel_exclusion = channel_exclusions.get(channel)
            direction = (
                as_str(registry[channel]["direction"])
                if channel in registry
                else "unknown"
            )
            if projection is not None:
                cells.append(projected_cell(channel, projection, source))
            elif exclusion is not None:
                cells.append(excluded_cell(channel, exclusion, source))
            elif channel_exclusion is not None:
                cells.append(excluded_cell(channel, channel_exclusion, source))
            elif direction == INBOUND_ONLY_DIRECTION:
                cells.append(emission_not_applicable_cell(channel))
            else:
                cells.append(missing_cell(channel, source))
        emissions.append({"name": emission, "cells": cells})

    return {
        "$schema": "projection-matrix.schema.json",
        "concept": concept,
        "generated_from": generated_from_sources(
            concepts_dir, definition_path, manifest_path, channels_path
        ),
        "channels": matrix_channels(channel_keys, channels),
        "actions": actions,
        "emissions": emissions,
    }


def generate_projection_matrices(concepts_dir: Path) -> list[dict[str, object]]:
    """Derive projection matrices for every surface manifest with a definition."""
    surfaces_dir = concepts_dir / "surfaces"
    if not surfaces_dir.is_dir():
        return []

    definition_paths = load_definition_paths(concepts_dir, "concept")
    channels_path = concepts_dir / "channels.json"
    if not channels_path.exists():
        channels_path = None

    matrices: list[dict[str, object]] = []
    for manifest_path in sorted(surfaces_dir.glob("*.json")):
        manifest = load_json(manifest_path)
        concept = as_str(manifest["concept"])
        definition_path = definition_paths.get(concept)
        if definition_path is None:
            continue
        matrices.append(
            generate_projection_matrix(
                concepts_dir, definition_path, manifest_path, channels_path
            )
        )
    return matrices


def write_projection_matrices(
    concepts_dir: Path,
    output_dir: Path | None = None,
) -> list[Path]:
    """Write derived projection matrices under concepts/projection-matrices/."""
    destination = output_dir or concepts_dir / "projection-matrices"
    destination.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for matrix in generate_projection_matrices(concepts_dir):
        name = as_str(matrix["concept"]).lower().replace(" ", "-")
        path = destination / f"{name}.json"
        path.write_text(json.dumps(matrix, indent=2) + "\n")
        written.append(path)
    return written


def projection_matrix_missing_cells(matrix: dict[str, object]) -> set[str]:
    concept = as_str(matrix["concept"])
    missing: set[str] = set()
    for row_kind in ("actions", "emissions"):
        target_kind = row_kind[:-1]
        for row_obj in as_list(matrix.get(row_kind, [])):
            row = as_dict(row_obj)
            name = as_str(row["name"])
            for cell_obj in as_list(row["cells"]):
                cell = as_dict(cell_obj)
                if cell.get("status") == "missing":
                    channel = as_str(cell["channel"])
                    missing.add(f"{concept}:{target_kind}:{channel}:{name}")
    return missing


def level_1_schema_validation(concepts_dir: Path, schemas_dir: Path) -> int:
    """Validate each file against its JSON Schema."""
    print("Level 1: Schema validation")
    failures = 0
    registry = build_schema_registry(schemas_dir)
    artifacts = discover_artifacts(concepts_dir, schemas_dir)
    for filepath, schema_path in artifacts.items():
        instance = load_json(filepath)
        schema = load_json(schema_path)
        label = str(filepath.relative_to(concepts_dir))
        try:
            validate(instance, schema, registry=registry)
            print_result(label, True)
        except ValidationError as e:
            print_result(label, False, e.message)
            failures += 1
    return failures


def level_2_cross_artifact(concepts_dir: Path, schemas_dir: Path) -> int:
    """Verify cross-artifact consistency."""
    print("\nLevel 2: Cross-artifact consistency")
    failures = 0

    dep_graph = load_json(concepts_dir / "dependency-graph.json")
    coherence = load_json(concepts_dir / "coherence.json")
    challenges_path = concepts_dir / "challenges.json"
    challenges = load_json(challenges_path) if challenges_path.exists() else None

    # Every seeded file must declare a recognized kind. Catches silent
    # misclassification before any downstream check filters by kind.
    seeded = iter_seeded_files(concepts_dir)
    valid_kinds = {"concept", "spec"}
    bad_kinds: dict[str, str] = {}
    for path, data in seeded:
        seed = as_dict(data["seed"])
        kind = seed.get("kind")
        label = str(path.relative_to(concepts_dir))
        if not isinstance(kind, str) or kind not in valid_kinds:
            bad_kinds[label] = repr(kind)
    passed = len(bad_kinds) == 0
    print_result(
        "Every seeded file has a recognized seed.kind",
        passed,
        f"bad: {bad_kinds}" if not passed else "",
    )
    failures += 0 if passed else 1

    definitions = load_definitions(concepts_dir, "concept")

    graph_concepts = {as_str(c) for c in as_list(dep_graph["concepts"])}
    graph_specs = {as_str(s) for s in as_list(dep_graph.get("specs", []))}
    def_concepts = set(definitions.keys())

    # Names match: every concept in dep graph has a definition
    missing_defs = graph_concepts - def_concepts
    passed = len(missing_defs) == 0
    print_result(
        "Dependency graph concepts have definitions",
        passed,
        f"missing: {missing_defs}" if not passed else "",
    )
    failures += 0 if passed else 1

    # Names symmetric: every definition appears in dep graph
    extra_defs = def_concepts - graph_concepts
    passed = len(extra_defs) == 0
    print_result(
        "All definitions appear in dependency graph",
        passed,
        f"extra: {extra_defs}" if not passed else "",
    )
    failures += 0 if passed else 1

    # Dependencies valid: every depends_on target exists in concepts or specs
    dep_targets = {
        as_str(as_dict(d)["depends_on"]) for d in as_list(dep_graph["dependencies"])
    }
    valid_targets = graph_concepts | graph_specs
    invalid_targets = dep_targets - valid_targets
    passed = len(invalid_targets) == 0
    print_result(
        "Dependency targets exist",
        passed,
        f"invalid: {invalid_targets}" if not passed else "",
    )
    failures += 0 if passed else 1

    # No circular dependencies (simple cycle detection)
    edges: dict[str, set[str]] = {c: set() for c in graph_concepts}
    for dep_obj in as_list(dep_graph["dependencies"]):
        dep = as_dict(dep_obj)
        edges[as_str(dep["concept"])].add(as_str(dep["depends_on"]))
    visited: set[str] = set()
    in_stack: set[str] = set()
    has_cycle = False

    def dfs(node: str) -> bool:
        visited.add(node)
        in_stack.add(node)
        for neighbor in edges.get(node, set()):
            if neighbor in in_stack:
                return True
            if neighbor not in visited and dfs(neighbor):
                return True
        in_stack.discard(node)
        return False

    for concept in graph_concepts:
        if concept not in visited and dfs(concept):
            has_cycle = True
            break
    passed = not has_cycle
    print_result("No circular dependencies", passed)
    failures += 0 if passed else 1

    # Coherence covers all concepts
    coherence_concepts = {as_str(c) for c in as_list(coherence["concepts"])}
    passed = coherence_concepts == graph_concepts
    print_result(
        "Coherence covers all concepts",
        passed,
        f"mismatch: {coherence_concepts ^ graph_concepts}" if not passed else "",
    )
    failures += 0 if passed else 1

    if challenges is not None:
        challenge_concepts = {as_str(c) for c in as_list(challenges["concepts"])}
        passed = challenge_concepts == graph_concepts
        print_result(
            "Challenges cover all concepts",
            passed,
            f"mismatch: {challenge_concepts ^ graph_concepts}" if not passed else "",
        )
        failures += 0 if passed else 1

        scenarios = [as_dict(s) for s in as_list(challenges["scenarios"])]

        unknown_refs: set[str] = set()
        for scenario in scenarios:
            for concept in as_list(scenario["concepts_involved"]):
                name = as_str(concept)
                if name not in graph_concepts:
                    unknown_refs.add(name)
        passed = len(unknown_refs) == 0
        print_result(
            "Challenge concepts_involved exist",
            passed,
            f"unknown: {unknown_refs}" if not passed else "",
        )
        failures += 0 if passed else 1

        ids = [as_str(s["id"]) for s in scenarios]
        duplicate_ids = {i for i in ids if ids.count(i) > 1}
        passed = len(duplicate_ids) == 0
        print_result(
            "Challenge scenario IDs unique",
            passed,
            f"duplicates: {duplicate_ids}" if not passed else "",
        )
        failures += 0 if passed else 1
    else:
        print_result("Challenges (skipped — no challenges.json)", True)

    lp_path = concepts_dir / "learning-path.json"
    learning_path = load_json(lp_path) if lp_path.exists() else None
    if learning_path is not None:
        all_nodes = graph_concepts | graph_specs
        tier_of: dict[str, int] = {}
        assumes_all: set[str] = set()
        path_nodes: set[str] = set()
        for tier_obj in as_list(learning_path["tiers"]):
            tier = as_dict(tier_obj)
            level = (
                int(as_str(tier["level"]))
                if not isinstance(tier["level"], int)
                else tier["level"]
            )
            for co_obj in as_list(tier["concepts"]):
                co = as_dict(co_obj)
                name = as_str(co["concept"])
                tier_of[name] = level
                path_nodes.add(name)
                assumes_all |= {as_str(a) for a in as_list(co.get("assumes", []))}

        # Covers all concepts (specs optional); no phantom nodes.
        missing = graph_concepts - path_nodes
        unknown = path_nodes - all_nodes
        passed = not missing and not unknown
        print_result(
            "Learning path covers all concepts",
            passed,
            f"missing: {missing} unknown: {unknown}" if not passed else "",
        )
        failures += 0 if passed else 1

        # Every assumes target is a known node.
        bad_assumes = assumes_all - all_nodes
        passed = len(bad_assumes) == 0
        print_result(
            "Learning path assumes resolve to known nodes",
            passed,
            f"unknown: {bad_assumes}" if not passed else "",
        )
        failures += 0 if passed else 1

        # No forward references: a dependent sits in a strictly later tier than
        # what it depends on. The dependency graph is the source of truth.
        violations: set[str] = set()
        for dep_obj in as_list(dep_graph["dependencies"]):
            dep = as_dict(dep_obj)
            c = as_str(dep["concept"])
            t = as_str(dep["depends_on"])
            if c in tier_of and t in tier_of and tier_of[c] <= tier_of[t]:
                violations.add(f"{c}@{tier_of[c]}<-{t}@{tier_of[t]}")
        passed = len(violations) == 0
        print_result(
            "Learning path tiers respect dependencies (no forward references)",
            passed,
            f"violations: {violations}" if not passed else "",
        )
        failures += 0 if passed else 1

        # Primitives are dependency roots (they depend on nothing).
        dep_sources = {
            as_str(as_dict(d)["concept"]) for d in as_list(dep_graph["dependencies"])
        }
        primitives = {as_str(p) for p in as_list(learning_path.get("primitives", []))}
        non_roots = primitives & dep_sources
        passed = len(non_roots) == 0
        print_result(
            "Learning path primitives are dependency roots",
            passed,
            f"non-roots: {non_roots}" if not passed else "",
        )
        failures += 0 if passed else 1
    else:
        print_result("Learning path (skipped — no learning-path.json)", True)

    idm_path = concepts_dir / "integrated-data-model.json"
    idm = load_json(idm_path) if idm_path.exists() else None
    if idm is not None:
        sources: set[str] = set()
        for ent_obj in as_list(idm["entities"]):
            ent = as_dict(ent_obj)
            sources |= {as_str(s) for s in as_list(ent["source_concepts"])}
        for rel_obj in as_list(idm["relations"]):
            sources.add(as_str(as_dict(rel_obj)["source_concept"]))

        # Every concept's micromodel is represented in the merged model.
        missing = graph_concepts - sources
        passed = len(missing) == 0
        print_result(
            "Integrated model covers all concepts",
            passed,
            f"missing: {missing}" if not passed else "",
        )
        failures += 0 if passed else 1

        # Every source concept named is a real concept (not a spec or typo).
        unknown = sources - graph_concepts
        passed = len(unknown) == 0
        print_result(
            "Integrated model sources are known concepts",
            passed,
            f"unknown: {unknown}" if not passed else "",
        )
        failures += 0 if passed else 1
    else:
        print_result(
            "Integrated data model (skipped — no integrated-data-model.json)", True
        )

    surfaces_dir = concepts_dir / "surfaces"
    manifests = (
        [load_json(p) for p in sorted(surfaces_dir.glob("*.json"))]
        if surfaces_dir.is_dir()
        else []
    )
    channels_path = concepts_dir / "channels.json"
    channels = load_json(channels_path) if channels_path.exists() else None

    if manifests:
        actions_by_concept: dict[str, set[str]] = {}
        emissions_by_concept: dict[str, set[str]] = {}
        state_by_concept: dict[str, set[str]] = {}
        for cname, cdef in definitions.items():
            actions_by_concept[cname] = {
                as_str(as_dict(a)["name"]) for a in as_list(cdef.get("actions", []))
            }
            emissions_by_concept[cname] = {
                as_str(as_dict(e)["name"]) for e in as_list(cdef.get("emissions", []))
            }
            state_by_concept[cname] = {
                as_str(as_dict(s)["name"]) for s in as_list(cdef.get("state", []))
            }

        registered: set[str] | None = None
        channel_directions: dict[str, str] = {}
        if channels is not None:
            registered = set()
            for channel_obj in as_list(channels["channels"]):
                channel_def = as_dict(channel_obj)
                key = as_str(channel_def["key"])
                registered.add(key)
                channel_directions[key] = as_str(channel_def["direction"])

        bad_action_refs: set[str] = set()
        bad_emission_refs: set[str] = set()
        bad_emission_directions: set[str] = set()
        bad_state_refs: set[str] = set()
        unregistered: set[str] = set()
        uncovered: set[str] = set()
        uncovered_emissions: set[str] = set()
        missing_target_surfaces: set[str] = set()
        saw_target_policy = False

        for manifest in manifests:
            concept = as_str(manifest["concept"])
            concept_actions = actions_by_concept.get(concept, set())
            concept_emissions = emissions_by_concept.get(concept, set())
            concept_state = state_by_concept.get(concept, set())
            surfaces = [as_dict(s) for s in as_list(manifest["surfaces"])]
            surfaced_channels = {as_str(s["channel"]) for s in surfaces}
            target_channels = {
                as_str(c) for c in as_list(manifest.get("target_channels", []))
            }
            channel_exclusions = [
                as_dict(e) for e in as_list(manifest.get("channel_exclusions", []))
            ]
            excluded_channels = {as_str(e["channel"]) for e in channel_exclusions}

            if target_channels or excluded_channels:
                saw_target_policy = True

            for channel in target_channels | excluded_channels:
                if registered is not None and channel not in registered:
                    unregistered.add(f"{concept}:{channel}")

            for channel in target_channels - excluded_channels - surfaced_channels:
                missing_target_surfaces.add(f"{concept}:{channel}")

            for surf in surfaces:
                channel = as_str(surf["channel"])
                if registered is not None and channel not in registered:
                    unregistered.add(f"{concept}:{channel}")
                afforded = {
                    as_str(as_dict(a)["action"]) for a in as_list(surf["actions"])
                }
                emitted = {
                    as_str(as_dict(e)["emission"])
                    for e in as_list(surf.get("emissions", []))
                }
                excluded = {
                    as_str(as_dict(e)["action"])
                    for e in as_list(surf.get("exclusions", []))
                }
                emission_excluded = {
                    as_str(as_dict(e)["emission"])
                    for e in as_list(surf.get("emission_exclusions", []))
                }
                for ref in afforded | excluded:
                    if ref not in concept_actions:
                        bad_action_refs.add(f"{concept}:{channel}:{ref}")
                for ref in emitted | emission_excluded:
                    if ref not in concept_emissions:
                        bad_emission_refs.add(f"{concept}:{channel}:{ref}")
                if (
                    emitted
                    and registered is not None
                    and not is_outbound(channel_directions.get(channel))
                ):
                    for ref in emitted:
                        bad_emission_directions.add(f"{concept}:{channel}:{ref}")
                for s_obj in as_list(surf["state"]):
                    comp = as_str(as_dict(s_obj)["component"])
                    if comp not in concept_state:
                        bad_state_refs.add(f"{concept}:{channel}:{comp}")
                for missing in concept_actions - (afforded | excluded):
                    uncovered.add(f"{concept}:{channel}:{missing}")
                outbound_capable = registered is None or is_outbound(
                    channel_directions.get(channel)
                )
                if outbound_capable:
                    for missing in concept_emissions - (emitted | emission_excluded):
                        uncovered_emissions.add(f"{concept}:{channel}:{missing}")

        passed = len(bad_action_refs) == 0
        print_result(
            "Surface affordances reference real actions",
            passed,
            f"unknown: {bad_action_refs}" if not passed else "",
        )
        failures += 0 if passed else 1

        passed = len(bad_emission_refs) == 0
        print_result(
            "Surface emission projections reference real emissions",
            passed,
            f"unknown: {bad_emission_refs}" if not passed else "",
        )
        failures += 0 if passed else 1

        passed = len(bad_emission_directions) == 0
        print_result(
            "Emission projections use outbound-capable channels",
            passed,
            f"invalid: {bad_emission_directions}" if not passed else "",
        )
        failures += 0 if passed else 1

        passed = len(bad_state_refs) == 0
        print_result(
            "Surface state references real components",
            passed,
            f"unknown: {bad_state_refs}" if not passed else "",
        )
        failures += 0 if passed else 1

        if registered is not None:
            passed = len(unregistered) == 0
            print_result(
                "Surface and target channels are registered in channels.json",
                passed,
                f"unregistered: {unregistered}" if not passed else "",
            )
            failures += 0 if passed else 1
        else:
            print_result(
                "Surface channels registered (skipped — no channels.json)", True
            )

        if saw_target_policy:
            passed = len(missing_target_surfaces) == 0
            print_result(
                "Target channels have surfaces or channel exclusions",
                passed,
                f"missing: {missing_target_surfaces}" if not passed else "",
            )
            failures += 0 if passed else 1
        else:
            print_result(
                "Target channel coverage (skipped — no target_channels policy)", True
            )

        passed = len(uncovered) == 0
        print_result(
            "Surface coverage: every action afforded or excluded per channel",
            passed,
            f"uncovered: {uncovered}" if not passed else "",
        )
        failures += 0 if passed else 1

        passed = len(uncovered_emissions) == 0
        print_result(
            "Emission coverage: every emission projected or excluded per outbound channel",
            passed,
            f"uncovered: {uncovered_emissions}" if not passed else "",
        )
        failures += 0 if passed else 1
    else:
        print_result("Surfaces (skipped — no surfaces/ manifests)", True)

    projection_dir = concepts_dir / "projection-matrices"
    if projection_dir.is_dir():
        missing_projection_cells: set[str] = set()
        for matrix_path in sorted(projection_dir.glob("*.json")):
            matrix = load_json(matrix_path)
            missing_projection_cells |= projection_matrix_missing_cells(matrix)

        passed = len(missing_projection_cells) == 0
        print_result(
            "Projection matrix coverage: no missing cells",
            passed,
            f"missing: {missing_projection_cells}" if not passed else "",
        )
        failures += 0 if passed else 1
    else:
        print_result(
            "Projection matrices (skipped — no projection-matrices/ artifacts)", True
        )

    return failures


def level_3_staleness(concepts_dir: Path, schemas_dir: Path) -> int:
    """Upstream-timestamp staleness check.

    A derived artifact must be at least as new as every artifact it derives
    from. Catches an edit that leaves a downstream artifact out of date because
    its stage was never re-run. Timestamp-based (file mtime); a content-hash
    variant can come later if mtime proves too coarse.
    """
    print("\nLevel 3: Staleness (upstream timestamps)")
    failures = 0

    def mtime(p: Path) -> float | None:
        return p.stat().st_mtime if p.exists() else None

    # Definition files (concept + spec), indexed by file stem for per-name views.
    def_paths: list[Path] = []
    stem_to_def: dict[str, Path] = {}
    for path, data in iter_seeded_files(concepts_dir):
        seed = as_dict(data.get("seed", {}))
        if seed.get("kind") in {"concept", "spec"}:
            def_paths.append(path)
            stem_to_def[path.stem] = path

    def check(downstream: Path, inputs: list[Path], label: str) -> None:
        nonlocal failures
        if not downstream.exists():
            print_result(f"{label} (skipped — absent)", True)
            return
        d = mtime(downstream) or 0.0
        offenders = sorted(p.name for p in inputs if (mtime(p) or 0.0) > d)
        passed = not offenders
        print_result(label, passed, f"older than: {offenders}" if not passed else "")
        failures += 0 if passed else 1

    dg = concepts_dir / "dependency-graph.json"
    check(dg, def_paths, "dependency-graph not older than any definition")
    for fname in ("coherence.json", "challenges.json", "learning-path.json"):
        check(concepts_dir / fname, [dg], f"{fname} not older than dependency-graph")
    check(
        concepts_dir / "integrated-data-model.json",
        [*def_paths, dg],
        "integrated-data-model not older than definitions or dependency-graph",
    )

    # Per-concept derived views.
    for sub in ("surfaces", "genericity"):
        d = concepts_dir / sub
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.json")):
            src = stem_to_def.get(f.stem)
            if src is not None:
                check(f, [src], f"{sub}/{f.name} not older than its definition")

    projection_dir = concepts_dir / "projection-matrices"
    if projection_dir.is_dir():
        for matrix_path in sorted(projection_dir.glob("*.json")):
            inputs: list[Path] = []
            matrix = load_json(matrix_path)
            generated_from = as_dict(matrix.get("generated_from", {}))
            for source in generated_from.values():
                resolved = resolve_artifact_source(as_str(source), concepts_dir)
                if resolved.exists():
                    inputs.append(resolved)
            check(
                matrix_path,
                inputs,
                f"projection-matrices/{matrix_path.name} not older than its inputs",
            )

    return failures


LEVELS = {
    1: level_1_schema_validation,
    2: level_2_cross_artifact,
    3: level_3_staleness,
}


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate concept artifacts against schemas.",
    )
    parser.add_argument(
        "concepts_dir",
        type=Path,
        help="Path to the concepts directory.",
    )
    parser.add_argument(
        "schemas_dir",
        type=Path,
        help="Path to the schemas directory.",
    )
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3],
        action="append",
        dest="levels",
        help="Validation level(s) to run (default: all). Repeatable.",
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    parsed = parse_args(args)
    concepts_dir: Path = parsed.concepts_dir.resolve()
    schemas_dir: Path = parsed.schemas_dir.resolve()
    levels: list[int] = sorted(parsed.levels) if parsed.levels else [1, 2, 3]

    failures = 0
    for level in levels:
        failures += LEVELS[level](concepts_dir, schemas_dir)

    print(f"\n{'All checks passed.' if failures == 0 else f'{failures} failure(s).'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
