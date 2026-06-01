---
id: LAYERED_UI_REVEAL
title: "Layered UI Reveal."
essence: "The UI is layered: base, chrome, surfaces, items, decoration. A JS console command strips the UI to one layer and lets the user re-add layers one at a time. Architectural visibility is a first-class debugging affordance."
related: [VISUAL_DEBUGGING, DEV_WORKFLOW, ANCESTRY_TRACING, INSET_VS_FLUSH_LAYOUT, EDGE_ALWAYS_CHROME, FLAT_CLASSED_FLEX_TREE]
---

A UI built from clearly-named structural layers can be debugged by stripping layers off, examining the base, and re-adding layers one at a time. The same property that makes a UI legible to humans makes it legible to instruments.

This principle codifies a contract: every UI exposes a JS console API that toggles visibility of named structural layers. Calling `ui.layer.only('base')` shows the viewport-locked shell. Calling `ui.layer.add('chrome')` adds the chrome. Each command is a step up the structural ladder.

## The layers

The default layer stack reflects the underlying structural principles:

| Layer | What it contains | Reveal signal |
|---|---|---|
| Base | The viewport-locked root container; `overflow: hidden` clipping; flex/grid distribution of fixed and flexible regions | Always present (the substrate) |
| Chrome | Header, footer, sidebars, status bars — the edge-occupying surfaces (see `EDGE_ALWAYS_CHROME`) | `ui.layer.add('chrome')` |
| Surfaces | Inset cards, flush lists, content panels — the structural surfaces inside the content region (see `INSET_VS_FLUSH_LAYOUT`) | `ui.layer.add('surfaces')` |
| Items | Rows, menu items, nav entries, table cells — the leaf content children | `ui.layer.add('items')` |
| Decoration | Hover states, focus rings, active indicators, transitions | `ui.layer.add('decoration')` |

Layers compose by addition. The base is always present; higher layers stack on top. `ui.layer.only(name)` is shorthand for `reset()` then `add(name)`.

## Implementation contract

The layer system is a console-callable API, not a build-time mode:

1. Exposes a `ui.layer` (or namespaced equivalent) object on `window`.
2. Provides `add(name)`, `remove(name)`, `only(name)`, `reset()`.
3. Toggles visibility via a single attribute on `:root` (`data-layers="base chrome"`), not by mutating individual elements.
4. Maps each layer name to a set of selectors or `[data-layer]` attributes — the mapping is mechanical, not magical, and lives in one file co-located with the layout.

The CSS for layer toggling lives in a dedicated `@layer debug` block that ships in production. The performance cost is negligible; the architectural visibility is large.

## Why this is a principle, not a tool

Most projects accumulate ad-hoc debugging tools: a CSS file that outlines every div, a console snippet that highlights flex containers, a screenshot script. These are personal artifacts: undocumented, undiscoverable, and stale the first time the project's structure shifts.

A layered reveal is *part of the project*. It's discoverable (typing `ui.` in the console autocompletes the API), versioned with the codebase, and survives refactors because the layer-to-selector mapping is part of the same file that defines the layout. When the structure changes, the layer mapping updates with it; the contract is preserved.

The layered reveal also doubles as a regression check: an automated test can call `ui.layer.only('base')` and assert the rendered DOM matches a known-good base layout. The reveal isn't only a debugging affordance; it's a structural assertion.

## Naming convention

Layer names mirror the structural-principle names (Base, Chrome, Surfaces, Items, Decoration). When a project introduces a new layer (e.g., Overlays for modals and toasts), it picks a name from the principles' vocabulary, not a project-specific shorthand. The shared name lets the layered reveal compose across applications built on the same design system.

## Relationship to other principles

- `VISUAL_DEBUGGING` is the broad principle that says debugging instruments belong in the project. This principle specializes it for structural layers.
- `DEV_WORKFLOW` and `BROWSER_AUTOMATION` describe the tooling around inspection. This principle slots into them as a concrete API.
- `EDGE_ALWAYS_CHROME` and `INSET_VS_FLUSH_LAYOUT` define what the chrome and surface layers contain. The layered reveal makes those definitions inspectable in the running UI.
- `FLAT_CLASSED_FLEX_TREE` makes the layer-to-selector mapping easy to write: every element has a class, so layer membership is one class match away.
- `ANCESTRY_TRACING` is the diagnostic principle for navigating the tree; the layered reveal is the navigational principle that lets the diagnostic run on the right slice.
