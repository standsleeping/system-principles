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
4. Export composition artifacts (dependency graph, coherence assessment including any `Demotion` entries, and the learning path).
5. Run schema validation on each file.
6. Run cross-artifact linting to verify consistency.

## Directory Structure

```
concepts/
  <concept-name>.json         # ConceptDefinition (one per concept)
  specs/
    <spec-name>.json          # SpecDefinition (one per spec)
  dependency-graph.json       # DependencyGraph (covers concepts and specs)
  channels.json               # ChannelRegistry (optional; channel kinds for surfaces)
  coherence.json              # CoherenceAssessment (with optional demotions)
  challenges.json             # ChallengeAssessment
  learning-path.json          # LearningPath (topological introduction order)
  integrated-data-model.json  # IntegratedDataModel (Stage 15; present once produced)
```

Optional subdirectories for larger systems:

```
concepts/
  surfaces/
    <concept-name>.json       # ConceptManifest (one per concept)
  projection-matrices/
    <concept-name>.json       # ProjectionMatrix (derived from definition + manifest + channels)
  genericity/
    <concept-name>.json       # GenericityAssessment (one per concept)
    specs/
      <spec-name>.json        # GenericityAssessment for specs
```

## Interaction Model

The durable conceptual model is:

```
Action is semantic.
Affordance is interface-specific.
Transport is mechanical.
Encoding is representational.
Surface is interactional.
Channel is operational packaging.
Projection is the relationship that binds them for one capability.
```

`channel` is therefore a named composite, not an atomic primitive: it bundles a transport, encoding, surface, and operational policy such as direction, sync shape, and auth model. Surface manifests should treat each per-channel action entry as an **affordance projection**: the canonical action stays on the concept definition, while the manifest records how that action is invoked on a particular channel.

## Schemas

JSON Schema files for every artifact type live in the `schemas/` subdirectory of this skill. Each file validates one artifact type:

| Schema file | Validates | Produced by |
|-------------|-----------|-------------|
| `concept-seed.schema.json` | ConceptSeed | concept-identification |
| `spec-seed.schema.json` | SpecSeed | concept-identification |
| `purpose.schema.json` | Purpose | concept-purpose |
| `operational-principle.schema.json` | OperationalPrinciple | operational-principle |
| `actions.schema.json` | Action[] | concept-actions |
| `emissions.schema.json` | Emission[] | concept-actions / surface-planning |
| `state.schema.json` | State | concept-state |
| `concept-definition.schema.json` | ConceptDefinition | concept-assembly |
| `concept-definition.partial.schema.json` | ConceptDefinition (draft, accreting) | stages 1–5 (incremental) |
| `spec-definition.schema.json` | SpecDefinition | spec-definition |
| `dependency-graph.schema.json` | DependencyGraph | dependency-mapping |
| `coherence-assessment.schema.json` | CoherenceAssessment (with optional Demotion[]) | coherence-analysis |
| `concept-manifest.schema.json` | ConceptManifest | surface-planning |
| `channel-registry.schema.json` | ChannelRegistry | surface-planning |
| `projection-matrix.schema.json` | ProjectionMatrix | generated from definitions, manifests, and channels |
| `genericity-assessment.schema.json` | GenericityAssessment | genericity-review |
| `challenge-assessment.schema.json` | ChallengeAssessment | challenge-testing |
| `learning-path.schema.json` | LearningPath | concept-ordering |
| `integrated-data-model.schema.json` | IntegratedDataModel | data-model-integration |

## Linting Rules

Verification is organized into two levels. Each level builds on the previous.

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
| **Surface actions valid** | Every affordance (and exclusion) in surface manifests references an action that exists in the concept's actions | manifests + definitions |
| **Surface emissions valid** | Every emission projection (and emission exclusion) in surface manifests references an emission that exists in the concept's emissions | manifests + definitions |
| **Emission direction valid** | Every projected emission uses a `system->caller` or `bi` channel when `channels.json` is present | manifests + channels |
| **Surface state valid** | Every state component in surface manifests exists in the concept's state | manifests + definitions |
| **Surface/target channels registered** | If `channels.json` exists, every surface, target channel, and channel exclusion references a registered key | manifests + channels |
| **Surface coverage** | For each surfaced channel, every concept action has an affordance or a documented exclusion | manifests + definitions |
| **Emission coverage** | For each outbound-capable surfaced channel, every concept emission has a projection or a documented exclusion | manifests + definitions + channels |
| **Target channels covered** | If a manifest declares `target_channels`, every target channel has a surface unless the channel is excluded with a reason | manifests + channels |
| **Projection matrix coverage** | If generated projection matrices exist, no action/emission cell has `status: "missing"` | projection-matrices |
| **Learning path covers all** | Every concept in dependency-graph.concepts appears in the learning path (specs optional); no phantom nodes | learning-path + dependency-graph |
| **Learning path assumes valid** | Every `assumes` target is a concept or spec in the dependency graph | learning-path + dependency-graph |
| **Learning path no forward refs** | For every dependency edge, the dependent sits in a strictly later tier than what it depends on | learning-path + dependency-graph |
| **Learning path primitives are roots** | Every `primitives` entry has no outgoing dependency (in-degree zero) | learning-path + dependency-graph |
| **Integrated model covers all** | Every concept in dependency-graph.concepts appears as a `source_concept` in some entity or relation | integrated-data-model + dependency-graph |
| **Integrated model sources valid** | Every `source_concept` named is a concept in the dependency graph | integrated-data-model + dependency-graph |

### Level 3: Staleness (upstream timestamps)

A derived artifact must be at least as new as every artifact it derives from. Catches an edit that leaves a downstream artifact out of date because its stage was never re-run. File-mtime based; skips any absent artifact.

| Rule | Check |
|------|-------|
| **dependency-graph fresh** | `dependency-graph.json` is not older than any concept/spec definition |
| **assessments fresh** | `coherence.json`, `challenges.json`, `learning-path.json` are not older than `dependency-graph.json` |
| **integrated model fresh** | `integrated-data-model.json` is not older than any definition or the dependency graph |
| **per-concept views fresh** | each `surfaces/<name>.json` and `genericity/<name>.json` is not older than its concept definition |
| **projection matrices fresh** | each `projection-matrices/<name>.json` is not older than its definition, surface manifest, or `channels.json` |

### Draft (accreting) definitions

While a concept is being built, `concepts/<name>.json` references `concept-definition.partial.schema.json` and may carry `draft: true` with only `seed` required (Stages 1–5 add fields incrementally). `concept-assembly` (Stage 6) completes it: switch its `$schema` to `concept-definition.schema.json` and drop `draft`. A `concepts/` whose files all reference the full schema (no drafts) is fully defined through Stage 6.

## Artifact

This skill produces: a `concepts/` directory containing validated JSON files, organized per the directory structure above. With incremental persistence, this skill no longer first-writes those files; stages persist their own artifacts as they complete, and this stage **organizes and runs the completeness/staleness checks** over them.

## Validation

A reference implementation of both levels lives in `scripts/validate_concepts.py`. It takes two required arguments: the path to the project's `concepts/` directory and the path to this skill's `schemas/` directory.

```
python scripts/validate_concepts.py <concepts_dir> <schemas_dir> [--level N ...]
```

Run specific levels with `--level` (repeatable), or omit for both. The script auto-discovers which schema validates each file by reading the `$schema` field in each JSON artifact.

Projection matrices are derived, not hand-authored. Generate them with:

```
python scripts/generate_projection_matrices.py <concepts_dir> [output_dir]
```

Optionally render the generated matrices as a static preview page with:

```
python scripts/render_projection_preview.py <concepts_dir_or_projection-matrices_dir> [output_html]
```

The preview renderer is a lightweight reference aid for inspecting the artifact
shape. The long-term dashboard UI belongs outside this skill.

Dependencies: `jsonschema`, `referencing` (must be in the project's dev dependencies).

Acceptance criteria:

- All files pass Level 1 (schema validation).
- All cross-references pass Level 2 (consistency).
- No concept definition file is missing for a concept that appears in the dependency graph.
