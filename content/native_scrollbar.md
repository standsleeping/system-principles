---
id: NATIVE_SCROLLBAR
title: "Native Scrollbar."
essence: "Scroll containers use `overflow: auto` and nothing else; the platform paints its own bar, themed by `color-scheme`. Never hide, tint, resize, or reserve a gutter for it. Overlay-scrollbar platforms get flush layout and zero shift for free; on classic platforms the bar rides the column edge — the accepted cost of respecting the user's OS scrollbar preference."
related: [NO_LAYOUT_SHIFT, SCROLL_CONTAINMENT, INSET_VS_FLUSH_LAYOUT, INDEPENDENT_VIEWPORT, BOUNDARY_OWNERSHIP]
---

The scrollbar belongs to the platform, not to the design system. The browser already renders a bar that follows the user's OS settings — overlay vs classic, increased size, high-contrast — and exposes it to assistive technology. The contract is to use that native bar and theme it, never to override it.

## The recipe

```css
:root {
  color-scheme: light dark;     /* the native bar (and other UA chrome) follows the theme */
}
.scroll-container {
  overflow-y: auto;             /* or overflow-x: auto for a horizontal leaf */
}
```

`overflow: auto` plus `color-scheme` on the root is the whole contract. No `scrollbar-width`, no `scrollbar-color`, no `scrollbar-gutter`, no `::-webkit-scrollbar`. Because `color-scheme` is what keeps the native bar on-theme, it is also what discharges the no-UA-default-color obligation for the scrollbar surface: the bar renders in the UA's themed palette, not a leaked default.

## Why native, not hidden or custom

Two earlier contracts are rejected by this one:

- **Hiding the bar** (`scrollbar-width: none` + `::-webkit-scrollbar { display: none }`) silently overrides the user's OS preference. macOS and Windows both expose an "always show scrollbars" accessibility setting; users who enable it need the affordance. Hiding also removes the only discoverability cue that a region scrolls. It is the least accessible option.
- **Custom-styling the bar** (tinted track/thumb via `scrollbar-color` or `::-webkit-scrollbar`) drifts from the platform, must be maintained per theme, and cannot match the OS's overlay / classic / high-contrast rendering.

## The flush tension and its resolution

A native classic scrollbar takes layout width, which appears to conflict with a flush, edge-to-edge layout. The conflict is bounded by platform:

| Platform | Behavior |
|---|---|
| Overlay (macOS default, touch) | Bar floats over content, reserves no space. Flush layout and zero layout shift hold for free. |
| Classic (Windows, most Linux, macOS "always show scrollbars") | Bar takes its width at the scroll container's inline-end edge when content overflows. |

`scrollbar-gutter: stable` would remove the classic-platform shift, but only by reserving an always-present inset strip — breaking the flush seam on *every* platform to fix a shift on *one*. This contract instead accepts the classic-platform bar as the platform-appropriate cost. Note that `scrollbar-gutter` reserves space inside the padding box but does not move the element's border: a flush *border* survives it; what it insets is content and any child-drawn full-bleed rule. The reason to forbid it here is the always-on inset strip, not the border.

## What this rules out

| Pattern | Why it's forbidden |
|---|---|
| `scrollbar-width: none` / `thin` | Hides or resizes the native bar; overrides OS preference |
| `::-webkit-scrollbar { ... }` | Replaces or suppresses the native bar |
| `scrollbar-color: ...` | Tints the bar off-platform; theme via `color-scheme` instead |
| `scrollbar-gutter: stable` | Reserves an always-on inset strip that breaks the flush seam |
| `overflow: scroll` | Forces a permanent bar even when nothing overflows; use `auto` |

## Enforcement

A grep-level lint forbids these patterns in `*.css` outside vendored / third-party trees:

```
overflow(-x|-y)?:\s*scroll
scrollbar-width:
scrollbar-color:
scrollbar-gutter:
::-webkit-scrollbar
```

The allowlist marker `/* scrollbar: ok */` covers the narrow exception: a component that owns its own viewport metaphor (a code editor, terminal, embedded map) and deliberately renders its own bar (see INDEPENDENT_VIEWPORT). Those are component-owned UIs, not layout chrome.

## What this principle replaces

This supersedes SCROLLBAR_HIDDEN_BY_DEFAULT (hide the bar everywhere) and, before it, both STABLE_SCROLLBAR_GUTTER (reserve a gutter) and a three-mode taxonomy (invisible-gutter / boundary-rail / transient-thumb). Each prior attempt made the design system *own* the scrollbar — by hiding it, reserving space for it, or restyling it. The native contract hands the bar back to the platform and themes it: simpler, and strictly more accessible.

## Relationship to other principles

- `NO_LAYOUT_SHIFT` holds on overlay platforms for free (the bar takes no space) and is consciously relaxed on classic platforms at the scroll container's edge — the accepted cost.
- `SCROLL_CONTAINMENT` still defines *where* scroll is allowed; this principle defines *how* those containers express it.
- `INSET_VS_FLUSH_LAYOUT` no longer needs a per-mode scrollbar choice; both modes use the native bar.
- `INDEPENDENT_VIEWPORT` is the narrow exception: a component owning its own viewport may render its own bar.
- `BOUNDARY_OWNERSHIP` is preserved: the column's edge is owned by the chrome's border, not by the bar; the native bar rides just inside that border.
