# Dependencies

## Visualizing Dependencies

Run the following command to visualize the dependency graph:

```bash
uv run pydeps src/[REPLACE] --max-module-depth=2 --rankdir RL --rmprefix [REPLACE].
```

Two-way arrows in the generated dependency graph indicate circular dependencies. There should be none.

## Subpackage Dependencies

To analyze dependencies within a specific subpackage:

```bash
uv run pydeps src/pkg --only pkg.<subpackage> --rmprefix pkg.<subpackage>. --rankdir RL -o <subpackage>_deps.svg
```

For example, to visualize the internal structure of `nodes.functions`:

```bash
uv run pydeps src/pkg --only pkg.nodes.functions --rmprefix pkg.nodes.functions. --rankdir RL -o nodes_functions_deps.svg
```

This focused analysis helps ensure that even within subpackages, we maintain clean dependencies and avoid circular references between internal modules.

### Internal Dependencies

To visualize only the dependencies between modules within a subpackage (excluding the `__init__.py`):

```bash
uv run pydeps src/pkg --only pkg.<subpackage> --exclude-exact pkg.<subpackage> --rmprefix pkg.<subpackage>. --rankdir RL -o <subpackage>_internal.svg
```

For example, to see only how the functions within `nodes.functions` depend on each other:

```bash
uv run pydeps src/pkg --only pkg.nodes.functions --exclude-exact pkg.nodes.functions --rmprefix pkg.nodes.functions. --rankdir RL -o nodes_functions_internal.svg
```

The `--exclude-exact` flag removes the package's `__init__.py` from the visualization, eliminating the noise of all modules pointing to it and showing only the actual inter-module dependencies.

### Understanding pydeps Visualization

In the generated SVG diagrams:

- **Blue boxes (rectangles)**: Modules that import other modules within the analyzed scope. These are typically integrators that orchestrate or use other modules.
- **Red ovals (ellipses)**: Modules with no dependencies within the analyzed scope. These are typically units or leaf nodes that are self-contained and don't import other modules from the package.

This visual distinction helps quickly identify which modules follow our units vs integrators pattern: red ovals often represent pure unit functions, while blue boxes often represent integrators that compose multiple units together.