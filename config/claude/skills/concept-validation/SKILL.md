---
name: concept-validation
description: Validate concept artifacts against schemas and cross-artifact consistency rules. Run after organizing artifacts or after implementation changes.
---

# Concept Validation

Verify that a project's concept artifacts are structurally valid and internally consistent.

## When to use

- After running `/concept-artifacts` to organize concept definitions into a directory
- After modifying concept definitions (adding concepts, changing actions, updating state)
- As a pre-commit or CI check to prevent concept drift

## Process

Run two levels of validation in order. Each level builds on the previous.

### Level 1: Schema validation

Validate each file in `concepts/` against its corresponding JSON Schema from the `concept-artifacts` skill's `schemas/` directory.

| File pattern | Schema |
|--------------|--------|
| Concept definition files at `concepts/<name>.json` (contain `"seed"` key with `kind: "concept"`) | `concept-definition.schema.json` |
| Spec definition files at `concepts/specs/<name>.json` (contain `"seed"` key with `kind: "spec"`) | `spec-definition.schema.json` |
| `dependency-graph.json` | `dependency-graph.schema.json` |
| `coherence.json` (with optional `demotions`) | `coherence-assessment.schema.json` |
| `challenges.json` | `challenge-assessment.schema.json` |
| `learning-path.json` (optional) | `learning-path.schema.json` |
| `integrated-data-model.json` (optional) | `integrated-data-model.schema.json` |
| `channels.json` (optional) | `channel-registry.schema.json` |
| Surface manifests at `surfaces/<name>.json` | `concept-manifest.schema.json` |
| Derived projection matrices at `projection-matrices/<name>.json` | `projection-matrix.schema.json` |

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
| Learning path covers all | Every `dependency-graph.concepts` entry appears in the learning path; no phantom nodes | learning-path + dependency-graph |
| Learning path assumes valid | Every `assumes` target exists in the dependency graph | learning-path + dependency-graph |
| Learning path no forward refs | Each dependent sits in a strictly later tier than what it depends on | learning-path + dependency-graph |
| Learning path primitives are roots | Every `primitives` entry has in-degree zero in the dependency graph | learning-path + dependency-graph |
| Integrated model covers all | Every `dependency-graph.concepts` entry appears as a `source_concept` in the integrated model | integrated-data-model + dependency-graph |
| Integrated model sources valid | Every `source_concept` is a concept in the dependency graph | integrated-data-model + dependency-graph |
| Surface affordances reference real actions | Every affordance/exclusion `action` exists in the concept's actions | manifests + definitions |
| Surface emission projections reference real emissions | Every emission projection/exclusion `emission` exists in the concept's emissions | manifests + definitions |
| Emission projections use outbound-capable channels | Every projected emission uses a `system->caller` or `bi` channel when `channels.json` exists | manifests + channels |
| Surface state references real components | Every surface `state[].component` exists in the concept's state | manifests + definitions |
| Surface/target channels registered | If `channels.json` exists, every surface `channel`, target channel, and channel exclusion references a registered key | manifests + channels |
| Target channels covered | If a manifest declares `target_channels`, every target channel has a surface or appears in `channel_exclusions` with a reason | manifests + channels |
| Surface coverage | For each surfaced channel, every concept action is afforded or excluded | manifests + definitions |
| Emission coverage | For each outbound-capable surfaced channel, every concept emission is projected or excluded | manifests + definitions + channels |
| Projection matrix coverage | If projection matrices exist, no action/emission cell has `status: "missing"` | projection-matrices |

### Level 3: Staleness (upstream timestamps)

A derived artifact must be at least as new as every artifact it derives from (file mtime). Catches a downstream artifact left out of date because its stage was not re-run after an upstream edit. Skips any absent artifact.

| Rule | Check |
|------|-------|
| dependency-graph fresh | `dependency-graph.json` not older than any concept/spec definition |
| assessments fresh | `coherence.json` / `challenges.json` / `learning-path.json` not older than `dependency-graph.json` |
| integrated model fresh | `integrated-data-model.json` not older than any definition or the dependency graph |
| per-concept views fresh | each `surfaces/<name>.json` and `genericity/<name>.json` not older than its concept definition |
| projection matrices fresh | each `projection-matrices/<name>.json` not older than its definition, surface manifest, or `channels.json` |

When incremental persistence is in use (see the `concept-design` Persistence protocol), Level 3 is the primary signal that a resumed run needs a stage re-run rather than a fresh start.

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
  ✗ Coherence covers all concepts — mismatch: {'Grid'}
  ...

N failure(s). / All checks passed.
```

## Validation

- Both levels should pass for a project's concept artifacts to be considered valid.
- Level 1 failures indicate malformed files; fix the JSON.
- Level 2 failures indicate inconsistency between artifacts; update the files that are out of sync.
