---
name: concept-validation
description: Validate concept artifacts against schemas and cross-artifact consistency rules. Run after organizing artifacts or after implementation changes.
---

# Concept Validation

Verify that a project's concept artifacts are structurally valid, internally consistent, and correctly linked to the codebase.

## When to use

- After running `/concept-artifacts` to organize concept definitions into a directory
- After modifying concept definitions (adding concepts, changing actions, updating state)
- After implementation changes that may affect action mapping entry points
- As a pre-commit or CI check to prevent concept drift

## Process

Run three levels of validation in order. Each level builds on the previous.

### Level 1: Schema validation

Validate each file in `concepts/` against its corresponding JSON Schema from the `concept-artifacts` skill's `schemas/` directory.

| File pattern | Schema |
|--------------|--------|
| Concept definition files at `concepts/<name>.json` (contain `"seed"` key with `kind: "concept"`) | `concept-definition.schema.json` |
| Spec definition files at `concepts/specs/<name>.json` (contain `"seed"` key with `kind: "spec"`) | `spec-definition.schema.json` |
| `dependency-graph.json` | `dependency-graph.schema.json` |
| `coherence.json` (with optional `demotions`) | `coherence-assessment.schema.json` |
| `challenges.json` | `challenge-assessment.schema.json` |
| `action-mapping.json` | `action-mapping.schema.json` |

Use the `jsonschema` library (Python) or `ajv` (Node) with a registry that can resolve `$ref` across schema files.

### Level 2: Cross-artifact consistency

Load all concept artifact files and verify cross-references.

| Rule | Check | Files |
|------|-------|-------|
| Seed kind present | Every file with a `seed` key declares a recognized `seed.kind` (`"concept"` or `"spec"`) | all definitions |
| Names match | Every concept in `dependency-graph.concepts` has a definition file | dependency-graph + definitions |
| Names symmetric | Every definition file's concept appears in `dependency-graph.concepts` | definitions + dependency-graph |
| Spec names match | Every spec in `dependency-graph.specs` has a SpecDefinition file under `specs/` | dependency-graph + spec definitions |
| Spec names symmetric | Every SpecDefinition file's spec appears in `dependency-graph.specs` | spec definitions + dependency-graph |
| Dependencies valid | Every `depends_on` target exists in `dependency-graph.concepts` or `.specs` | dependency-graph |
| No circular dependencies | The dependency graph is a DAG | dependency-graph |
| Spec referenced_by valid | Every concept named in a SpecDefinition's `referenced_by` exists | spec definitions + concept definitions |
| Spec references reciprocated | Every concept named in a Spec's `referenced_by` has a state component or action that mentions the Spec | spec definitions + concept definitions |
| Spec has ≥2 references | Every SpecDefinition's `referenced_by` list has at least two entries (Spec test #1) | spec definitions |
| Demotions resolve | Every `coherence.demotions[].from_concept` names a concept that is no longer present in `concepts/` (the file was reclassified or removed) | coherence + definitions |
| Coherence covers all | `coherence.concepts` matches `dependency-graph.concepts` | coherence + dependency-graph |
| Challenges cover all | `challenges.concepts` matches `dependency-graph.concepts` | challenges + dependency-graph |
| Challenge concepts exist | Every `concepts_involved` entry in `challenges.scenarios` is in `dependency-graph.concepts` | challenges + dependency-graph |
| Challenge IDs unique | No duplicate `scenario.id` within `challenges.scenarios` | challenges |
| Mapping concepts match | `action-mapping.concepts` matches `dependency-graph.concepts` | action-mapping + dependency-graph |
| Mapping actions exist | Every `mapping.action` exists in that concept's actions list | action-mapping + definitions |
| Mapping complete | Every (concept, action) pair in definitions has exactly one mapping | action-mapping + definitions |
| No orphan mappings | No mapping references a non-existent concept or action | action-mapping + definitions |

### Level 3: Codebase verification

For every action mapping where `implementation.type` is `"code"`:

| Rule | Check |
|------|-------|
| Entry points resolve | `entry_point` is importable as `module:function` |
| Called functions exist | Each entry in `calls` is importable as `module:function` |

Verification: split on `:`, import the module, check `hasattr` for the function.

## Output

This skill prints a transient validation report to stdout. Do not persist it. The report is a snapshot of one validator run; rerunning `validate_concepts.py` is the source of truth and the report decays the moment any artifact changes. Surface the report in the conversation; do not write it to `concepts/VALIDATION.md` or any other file.

If a validator run reveals upstream patches needed in another skill (e.g. a missing `$schema` field, a discovery bug), record those in the patched skill's git history, not in a per-project memo.

Report format:

```
Level 1: Schema validation
  ✓ grid.json
  ✓ observation.json
  ✗ dependency-graph.json — <error message>
  ...

Level 2: Cross-artifact consistency
  ✓ Names match
  ✗ Mapping complete — missing: {('Grid', 'view')}
  ...

Level 3: Codebase verification
  ✓ compgrid.main:main
  ...

N failure(s). / All checks passed.
```

## Validation

- All three levels should pass for a project's concept artifacts to be considered valid.
- Level 1 failures indicate malformed files; fix the JSON.
- Level 2 failures indicate inconsistency between artifacts; update the files that are out of sync.
- Level 3 failures indicate concept drift from implementation; update either the action mapping or the code.
