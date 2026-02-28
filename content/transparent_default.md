---
id: TRANSPARENT_DEFAULT
title: "Transparent by Default."
essence: "Default to transparent backgrounds on small elements; reserve background color for major containers."
---

Small UI elements should not compete for attention:

1. Badges, labels, and inline elements have transparent backgrounds
2. Remove padding and border-radius from small text elements
3. Reserve background colors for major container elements
4. Use white backgrounds for subtle section separation

This reduces visual noise and lets content breathe.

**Exception: sticky and fixed elements.** Any element with `position: sticky` or `position: fixed` needs an opaque background, even if it would otherwise be transparent. Content scrolling beneath a transparent sticky element is visible and distracting. See LAYOUT_QUIRKS.