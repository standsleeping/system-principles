---
name: concept-artifacts
description: Organize concept design outputs into a structured directory with JSON schemas and linting rules for automated verification.
---

# Concept Artifacts

Organize the outputs of the concept design workflow into a well-structured project directory. Each artifact is a JSON file that validates against a schema. Cross-artifact consistency is verifiable without human analysis.

## When to use

- After completing the concept design workflow (or any subset of it)
- When setting up a new project that will track its concept definitions as data
- When auditing whether concept artifacts are complete and internally consistent

## Process

1. Create a `concepts/` directory in the project root.
2. For each concept, export its `ConceptDefinition` as a JSON file under `concepts/`.
3. For each spec, export its `SpecDefinition` as a JSON file under `concepts/specs/`.
4. Export composition artifacts (dependency graph, coherence assessment, including any `Demotion` entries).
5. Export the action mapping, connecting concept actions to surfaces and implementations.
6. Run schema validation on each file.
7. Run cross-artifact linting to verify consistency.

## Directory Structure

```
concepts/
  <concept-name>.json         # ConceptDefinition (one per concept)
  specs/
    <spec-name>.json          # SpecDefinition (one per spec)
  dependency-graph.json       # DependencyGraph (covers concepts and specs)
  coherence.json              # CoherenceAssessment (with optional demotions)
  challenges.json             # ChallengeAssessment
  action-mapping.json         # ActionMapping
```

Optional subdirectories for larger systems:

```
concepts/
  surfaces/
    <concept-name>.json       # ConceptManifest (one per concept)
  genericity/
    <concept-name>.json       # GenericityAssessment (one per concept)
    specs/
      <spec-name>.json        # GenericityAssessment for specs
```

## Schemas

JSON Schema files for every artifact type live in the `schemas/` subdirectory of this skill. Each file validates one artifact type:

| Schema file | Validates | Produced by |
|-------------|-----------|-------------|
| `concept-seed.schema.json` | ConceptSeed | concept-identification |
| `spec-seed.schema.json` | SpecSeed | concept-identification |
| `purpose.schema.json` | Purpose | concept-purpose |
| `operational-principle.schema.json` | OperationalPrinciple | operational-principle |
| `actions.schema.json` | Action[] | concept-actions |
| `state.schema.json` | State | concept-state |
| `concept-definition.schema.json` | ConceptDefinition | concept-assembly |
| `spec-definition.schema.json` | SpecDefinition | spec-definition |
| `dependency-graph.schema.json` | DependencyGraph | dependency-mapping |
| `coherence-assessment.schema.json` | CoherenceAssessment (with optional Demotion[]) | coherence-analysis |
| `concept-manifest.schema.json` | ConceptManifest | surface-planning |
| `genericity-assessment.schema.json` | GenericityAssessment | genericity-review |
| `challenge-assessment.schema.json` | ChallengeAssessment | challenge-testing |
| `action-mapping.schema.json` | ActionMapping | concept-artifacts (this skill) |

## Linting Rules

Verification is organized into three levels. Each level builds on the previous.

### Level 1: Schema validation

Each file validates against its corresponding JSON Schema. This is structural validation: required fields present, types correct, enums valid.

Run with any JSON Schema validator (e.g., `jsonschema` for Python, `ajv` for Node).

### Level 2: Cross-artifact consistency

These rules verify that artifacts reference each other correctly. They require loading multiple files.

| Rule | Check | Files involved |
|------|-------|----------------|
| **Seed kind present** | Every file with a `seed` key declares a recognized `seed.kind` (`"concept"` or `"spec"`) | all definitions |
| **Names match** | Every concept name in dependency-graph.concepts has a ConceptDefinition file | dependency-graph + definitions |
| **Names symmetric** | Every ConceptDefinition file's concept name appears in dependency-graph.concepts | definitions + dependency-graph |
| **Spec names match** | Every spec name in dependency-graph.specs has a SpecDefinition file under specs/ | dependency-graph + spec definitions |
| **Spec names symmetric** | Every SpecDefinition file's spec name appears in dependency-graph.specs | spec definitions + dependency-graph |
| **Dependencies valid** | Every depends_on target exists in dependency-graph.concepts or .specs | dependency-graph |
| **No circular dependencies** | The dependency graph is a DAG | dependency-graph |
| **Spec referenced_by valid** | Every concept named in a SpecDefinition's referenced_by exists | spec definitions + concept definitions |
| **Spec references reciprocated** | Every concept named in a Spec's referenced_by has a state component or action that mentions the Spec | spec definitions + concept definitions |
| **Spec has ≥2 references** | Every SpecDefinition's referenced_by list has at least two entries (Spec test #1) | spec definitions |
| **Demotions resolve** | Every Demotion.from_concept names a ConceptDefinition that no longer exists in concepts/ (because it was reclassified) and either appears as a SpecDefinition under specs/ or is absent (if dropped) | coherence + definitions |
| **Coherence covers all** | coherence.concepts matches dependency-graph.concepts | coherence + dependency-graph |
| **Challenges cover all** | challenges.concepts matches dependency-graph.concepts | challenges + dependency-graph |
| **Challenge concepts exist** | Every concepts_involved entry in challenges.scenarios is in dependency-graph.concepts | challenges + dependency-graph |
| **Challenge IDs unique** | No duplicate scenario.id within challenges.scenarios | challenges |
| **Mapping concepts match** | action-mapping.concepts matches dependency-graph.concepts | action-mapping + dependency-graph |
| **Mapping actions exist** | Every mapping.action exists in that concept's actions list | action-mapping + definitions |
| **Mapping complete** | Every (concept, action) pair in definitions has exactly one mapping | action-mapping + definitions |
| **No orphan mappings** | No mapping references a non-existent concept or action | action-mapping + definitions |
| **Surface actions valid** | Every action in surface manifests exists in the concept's actions | manifests + definitions |
| **Surface state valid** | Every state component in surface manifests exists in the concept's state | manifests + definitions |

### Level 3: Codebase verification

These rules verify that implementation references in the action mapping resolve to actual code.

| Rule | Check | Requires |
|------|-------|----------|
| **Entry points resolve** | If implementation.type is "code", entry_point is importable | action-mapping + codebase |
| **Called functions exist** | If implementation.calls are specified, each is importable | action-mapping + codebase |

Entry points and calls use `module:function` notation (e.g., `compgrid.main:main`). Verification attempts to import the module and check for the function attribute.

## Artifact

This skill produces: a `concepts/` directory containing validated JSON files, organized per the directory structure above.

## Validation

A reference implementation of all three levels lives in `scripts/validate_concepts.py`. It takes two required arguments: the path to the project's `concepts/` directory and the path to this skill's `schemas/` directory.

```
python scripts/validate_concepts.py <concepts_dir> <schemas_dir> [--level N ...]
```

Run specific levels with `--level` (repeatable), or omit for all three. The script auto-discovers which schema validates each file by reading the `$schema` field in each JSON artifact.

Dependencies: `jsonschema`, `referencing` (must be in the project's dev dependencies).

Acceptance criteria:

- All files pass Level 1 (schema validation).
- All cross-references pass Level 2 (consistency).
- If action mapping includes code implementations, Level 3 passes (codebase verification).
- No concept definition file is missing for a concept that appears in the dependency graph.
- The action mapping has exactly one entry per (concept, action) pair.
