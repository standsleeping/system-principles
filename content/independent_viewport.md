---
id: INDEPENDENT_VIEWPORT
title: "Independent Viewport, Not Clipped Content."
essence: "Inner scroll regions are for content with its own interaction model. Never clip flowing content into a nested scroll container."
related: [SCROLL_CONTAINMENT, VIEWPORT_LOCKED, NO_LAYOUT_SHIFT]
---

Once SCROLL_CONTAINMENT establishes which leaf regions scroll, the question remains: can content *within* those regions introduce its own scroll? The answer is rarely, and only when the inner region is a distinct viewport with its own interaction model.

**The distinction:**

| Pattern | Example | Scroll? |
|---------|---------|---------|
| Independent viewport | Code editor, map embed, terminal, chat log | Yes: own interaction model, own scroll context |
| Clipped content | Table with `max-height`, long list with `overflow-y: auto`, prose in a fixed box | No: let it flow in the parent scroll |

**Why clipped content fails:**

1. Scroll-hijacking: the user scrolls the page but hits the inner region, and their scroll is captured (Baymard research: 26% of major sites get this wrong)
2. Hidden scrollbars: macOS and mobile OS hide inactive scrollbars, so users cannot tell the region scrolls
3. Accessibility: nested scrollable regions create exponential focus complexity, break screen reader mode switching, and disorient magnification users

**Three conditions for inner scroll:**

1. The inner region has its own interaction model (not just clipped prose or data)
2. The region does not fill the viewport; the user can scroll the page around it
3. The scrollbar is discoverable (fade gradients, scroll indicators) or the content type implies scrolling (terminal, editor)

**When inner scroll is used:**

- Apply `overscroll-behavior: contain` to prevent scroll-chaining to the parent
- Ensure the region is keyboard-accessible (`tabindex="0"`, arrow key scrolling)
- Test with macOS "Always show scroll bars" enabled

**Anti-patterns:**

- A data table clipped at a fixed height inside a scrollable page (clip the content, gain nothing)
- A dropdown filter list with `max-height` and `overflow-y: auto` (truncation or progressive disclosure is better)
- Any `overflow: auto` added solely to save vertical space
