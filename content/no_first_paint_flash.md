---
id: NO_FIRST_PAINT_FLASH
title: "No First-Paint Flash."
essence: "State that must be correct when the page first paints — theme, color scheme, persisted geometry — is established by a render-blocking script in the head, before any deferred or module JavaScript. Deferred code reflects that state; it never establishes it."
related: [NO_LAYOUT_SHIFT, HYDRATION_RESERVES_GEOMETRY, TOKEN_DRIVEN_DESIGN, STATE_BELONGS_TO_INTERACTIVE]
---

A page that reads a persisted preference — dark mode, color theme, saved panel widths — and applies it in deferred or module JavaScript paints the default first, then corrects itself. The user sees a flash of the wrong theme on every load. This is **FOUC** (flash of unstyled content), and it is not a timing accident you can tune away; it is structural.

## Why it is structural

`<script type="module">` and `<script defer>` execute *after* the document is parsed and, in practice, after first paint. `load` handlers and `ResizeObserver` callbacks run later still. Any code in those positions that sets a render-affecting attribute is, by definition, too late: the browser has already painted a frame with the default, and changing the attribute repaints a visibly different frame.

The only code that runs before first paint is a synchronous, render-blocking script in `<head>`. So that is where first-paint state must be established.

```html
<head>
  <!-- runs before the body paints; no flash -->
  <script>
    try {
      var lum = localStorage.getItem('app-luminance');
      if (lum === 'dark' || lum === 'light') document.documentElement.setAttribute('data-luminance', lum);
      var theme = localStorage.getItem('app-color-theme');
      if (theme) document.documentElement.setAttribute('data-color-theme', theme);
    } catch (e) {}
  </script>
  <link rel="stylesheet" href="tokens.css">
</head>
```

## Establishing state is not the same as rendering the control

A persisted preference has two responsibilities with two different lifetimes:

**Establishing** the state — must happen at frame 0, synchronously, at the document level.

**Rendering the control** that mutates it (the theme toggle, the density switch) — can happen whenever, asynchronously, lazily.

Fusing them is the trap. When the theme is applied as a side effect of mounting the toggle *component*, a frame-0 obligation inherits the component's mount time — and if that mount sits behind a network fetch or a dynamic import, the wrong theme persists for the whole round-trip. Split the two: the head bootstrap owns the attributes; the control reads the already-established state and only writes on user action (see STATE_BELONGS_TO_INTERACTIVE).

## What belongs in the bootstrap

Anything the first painted frame must get right: luminance / color-scheme, color theme, persisted layout geometry (panel widths, collapsed rails — see HYDRATION_RESERVES_GEOMETRY), and a reduced-motion or high-contrast override if you honor a stored one. All of it reads from one synchronous block, not from whichever component happens to toggle each piece.

Prefer mechanisms the browser resolves at paint time. `color-scheme: light dark` with `light-dark()` colors needs no script for the *follow-the-OS* case; the bootstrap is only needed when the user has overridden the OS default.

## Test

Throttle the network and CPU, then reload. If any color or geometry visibly changes after the first frame, the establishing code is in the wrong place — move it into the head bootstrap. A headless audit can assert the same property mechanically: the expected `data-*` attributes are present on the document element *before* hydration, not after settle.
