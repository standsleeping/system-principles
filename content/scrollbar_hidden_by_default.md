---
id: SCROLLBAR_HIDDEN_BY_DEFAULT
title: "Scrollbars Hidden by Default."
essence: "Scroll containers scroll, but never paint a visible bar. A two-line recipe (`scrollbar-width: none` plus `::-webkit-scrollbar { display: none }`) guarantees zero-width gutter on every platform, so layout never shifts and children always paint to the column edge."
related: [NO_LAYOUT_SHIFT, SCROLL_CONTAINMENT, INSET_VS_FLUSH_LAYOUT, INDEPENDENT_VIEWPORT, BOUNDARY_OWNERSHIP]
---

A visible scrollbar inside a layout container is a structural decision, not a stylistic one. Whether it paints, when it paints, and how wide it paints all leak into the surrounding geometry: borders stop short, tinted surfaces meet untinted gutters with no separator, content reflows when overflow toggles. The cleanest contract is that the bar never paints at all.

## The recipe

```css
.scroll-container {
  overflow-y: auto;
  scrollbar-width: none;            /* Firefox 64+ */
}
.scroll-container::-webkit-scrollbar {
  display: none;                    /* Chromium, Safari, Edge */
}
```

The container scrolls via every input modality (wheel, trackpad, touch, keyboard, focus-into-view) but never renders a visible bar. Because no bar is rendered, no gutter is ever reserved, and layout cannot shift between scrollable and non-scrollable states. Children always span the full content-box width.

## What this rules out

Every failure mode below is a regression vector this principle closes:

| Failure mode | Why it can't happen |
|---|---|
| Bar visible against a tinted child surface | No bar rendered, ever |
| Bar shifts content when overflow toggles | No bar takes width, ever |
| Borders or backgrounds stop short of the column edge | Children always have the full width to paint into |
| Custom track/thumb colors drift from theme | No custom colors to maintain |
| `scrollbar-gutter: stable` reserves an empty channel against a different-shade neighbour | No gutter to reserve |
| macOS overlay vs Windows classic divergence | Both UAs render no bar |
| Two scrollbar modes (boundary-rail vs invisible-gutter) confused at a layout boundary | One mode, no decision to get wrong |
| `scrollbar-color` / `scrollbar-width` cascade interactions | `scrollbar-width: none` short-circuits the cascade |

There is no `@supports` query needed, no platform branching, no light/dark coupling. Both declarations have been in WHATWG and shipping UAs for years.

## The one trade-off

The visual indicator that the container scrolls is gone. For most cases this is fine:

- **Focusable children.** Tab navigation auto-scrolls focus into view. Sidebar nav, table rows, list items already have this for free.
- **Wheel and trackpad.** Work without a visible bar.
- **Touch.** Swipe is the affordance; the bar was never doing work here anyway.
- **Keyboard.** `Page Down`, arrow keys (when focus is inside), `Home`/`End`, `Space` all work natively on overflowed containers.

Where a "more below" cue genuinely matters, the supplement is a CSS mask-image fade on the container, gated on `@supports (mask-image: ...)`. This is a one-line addition per container and is independent of the scrollbar config — it does not reintroduce any of the failure modes above.

## What this principle replaces

This principle subsumes an earlier two-mode taxonomy (boundary-rail vs invisible-gutter) and an earlier companion principle (STABLE_SCROLLBAR_GUTTER). Both were attempts to make a visible bar coexist with a flush layout. The taxonomy required choosing the right mode at every scroll container; the companion required reserving a gutter to keep widths stable; each created its own failure shape. Hiding the bar collapses both into a single rule that does not require a decision.

## Enforcement

A grep-level lint forbids these patterns in `*.css` outside vendored / third-party trees:

```
overflow-y: scroll
overflow-x: scroll
scrollbar-gutter:
::-webkit-scrollbar(?!\s*\{[^}]*display:\s*none)
scrollbar-width:\s*(?!none)
scrollbar-color:
```

The `::-webkit-scrollbar` allowance is narrow on purpose: the only legal block under that selector is `{ display: none }`. Anything else (custom track color, custom width, custom thumb radius) reintroduces a visible bar and the regression vectors above.

This is the part that makes the rule *foolproof* rather than *easy to follow today*. Without enforcement, every refactor risks a copy-paste of the old patterns — the lint catches them at PR time, before the visual regression lands.

## Relationship to other principles

- `NO_LAYOUT_SHIFT` is automatically satisfied by hidden bars: shifts from overflow toggling cannot happen if no bar takes width.
- `SCROLL_CONTAINMENT` still defines *where* scroll is allowed (sidebars, the center content, individual leaf elements like wide tables). This principle defines *how* those containers express scrolling.
- `INSET_VS_FLUSH_LAYOUT` no longer needs to pick a scrollbar mode per layout; both modes use the hidden bar.
- `INDEPENDENT_VIEWPORT` is the narrow exception: components with their own interaction model (code editors, terminals, embedded maps) may render their own scroll affordance, since the component itself owns the viewport metaphor. Those are vendored or component-owned UIs, not layout chrome.
- `BOUNDARY_OWNERSHIP` is preserved: the column's right edge is owned by the chrome's border (a 1px rule), not by a scrollbar that may or may not appear.
