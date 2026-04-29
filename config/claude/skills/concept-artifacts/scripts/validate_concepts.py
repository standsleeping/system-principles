"""Validate concept artifacts against schemas and cross-artifact consistency rules.

Usage: python validate_concepts.py <concepts_dir> <schemas_dir> [--level N ...]

Dependencies: jsonschema, referencing
"""

import argparse
import importlib
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


def discover_artifacts(concepts_dir: Path, schemas_dir: Path) -> dict[Path, Path]:
    """Map each concept file to its schema by reading the $schema field."""
    mapping: dict[Path, Path] = {}
    for path in sorted(concepts_dir.glob("*.json")):
        data = load_json(path)
        schema_ref = data.get("$schema")
        if schema_ref is None:
            print_result(path.name, False, "no $schema field, skipping")
            continue
        schema_path = schemas_dir / as_str(schema_ref)
        if not schema_path.exists():
            print_result(path.name, False, f"schema not found: {schema_ref}")
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
        try:
            validate(instance, schema, registry=registry)
            print_result(filepath.name, True)
        except ValidationError as e:
            print_result(filepath.name, False, e.message)
            failures += 1
    return failures


def level_2_cross_artifact(concepts_dir: Path, schemas_dir: Path) -> int:
    """Verify cross-artifact consistency."""
    print("\nLevel 2: Cross-artifact consistency")
    failures = 0

    dep_graph = load_json(concepts_dir / "dependency-graph.json")
    coherence = load_json(concepts_dir / "coherence.json")
    mapping = load_json(concepts_dir / "action-mapping.json")
    challenges_path = concepts_dir / "challenges.json"
    challenges = load_json(challenges_path) if challenges_path.exists() else None

    # Load all concept definitions
    definitions: dict[str, dict[str, object]] = {}
    for path in concepts_dir.glob("*.json"):
        data = load_json(path)
        if "seed" in data:
            definitions[as_str(as_dict(data["seed"])["name"])] = data

    graph_concepts = {as_str(c) for c in as_list(dep_graph["concepts"])}
    def_concepts = set(definitions.keys())
    mapping_concepts = {as_str(c) for c in as_list(mapping["concepts"])}

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

    # Dependencies valid: every depends_on target exists
    dep_targets = {
        as_str(as_dict(d)["depends_on"]) for d in as_list(dep_graph["dependencies"])
    }
    invalid_targets = dep_targets - graph_concepts
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

    # Mapping concepts match
    passed = mapping_concepts == graph_concepts
    print_result(
        "Mapping concepts match dependency graph",
        passed,
        f"mismatch: {mapping_concepts ^ graph_concepts}" if not passed else "",
    )
    failures += 0 if passed else 1

    # Build expected (concept, action) pairs from definitions
    expected_pairs: set[tuple[str, str]] = set()
    for concept_name, defn in definitions.items():
        for action in as_list(defn["actions"]):
            expected_pairs.add((concept_name, as_str(as_dict(action)["name"])))

    # Build actual (concept, action) pairs from mapping
    actual_pairs: set[tuple[str, str]] = set()
    for m_obj in as_list(mapping["mappings"]):
        m = as_dict(m_obj)
        actual_pairs.add((as_str(m["concept"]), as_str(m["action"])))

    # Mapping actions exist in definitions
    orphan_mappings = actual_pairs - expected_pairs
    passed = len(orphan_mappings) == 0
    print_result(
        "No orphan mappings",
        passed,
        f"orphans: {orphan_mappings}" if not passed else "",
    )
    failures += 0 if passed else 1

    # Mapping complete: every (concept, action) has a mapping
    missing_mappings = expected_pairs - actual_pairs
    passed = len(missing_mappings) == 0
    print_result(
        "Mapping complete (all actions covered)",
        passed,
        f"missing: {missing_mappings}" if not passed else "",
    )
    failures += 0 if passed else 1

    # No duplicate mappings
    pairs_list: list[tuple[str, str]] = [
        (as_str(as_dict(m)["concept"]), as_str(as_dict(m)["action"]))
        for m in as_list(mapping["mappings"])
    ]
    duplicates = {p for p in pairs_list if pairs_list.count(p) > 1}
    passed = len(duplicates) == 0
    print_result(
        "No duplicate mappings",
        passed,
        f"duplicates: {duplicates}" if not passed else "",
    )
    failures += 0 if passed else 1

    return failures


def level_3_codebase(concepts_dir: Path, schemas_dir: Path) -> int:
    """Verify that code entry points are importable."""
    print("\nLevel 3: Codebase verification")
    failures = 0
    mapping = load_json(concepts_dir / "action-mapping.json")

    for m_obj in as_list(mapping["mappings"]):
        m = as_dict(m_obj)
        impl = as_dict(m["implementation"])
        if impl["type"] != "code":
            continue

        entry = as_str(impl.get("entry_point", ""))
        calls = as_list(impl.get("calls", []))
        targets = [entry] + [as_str(c) for c in calls]

        for target in targets:
            if not target:
                continue
            module_path, func_name = target.rsplit(":", 1)
            try:
                mod = importlib.import_module(module_path)
                passed = hasattr(mod, func_name)
                print_result(
                    target,
                    passed,
                    "" if passed else f"function '{func_name}' not found in module",
                )
            except ImportError as e:
                print_result(target, False, f"import failed: {e}")
                failures += 1
                continue
            failures += 0 if passed else 1

    if failures == 0 and not any(
        as_dict(m)["implementation"]
        for m in as_list(mapping["mappings"])
        if as_dict(as_dict(m)["implementation"])["type"] == "code"
    ):
        print("  (no code implementations to verify)")

    return failures


LEVELS = {
    1: level_1_schema_validation,
    2: level_2_cross_artifact,
    3: level_3_codebase,
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
