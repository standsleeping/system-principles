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
        if concept not in visited:
            if dfs(concept):
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

    return failures


LEVELS = {
    1: level_1_schema_validation,
    2: level_2_cross_artifact,
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
        choices=[1, 2],
        action="append",
        dest="levels",
        help="Validation level(s) to run (default: all). Repeatable.",
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    parsed = parse_args(args)
    concepts_dir: Path = parsed.concepts_dir.resolve()
    schemas_dir: Path = parsed.schemas_dir.resolve()
    levels: list[int] = sorted(parsed.levels) if parsed.levels else [1, 2]

    failures = 0
    for level in levels:
        failures += LEVELS[level](concepts_dir, schemas_dir)

    print(f"\n{'All checks passed.' if failures == 0 else f'{failures} failure(s).'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
