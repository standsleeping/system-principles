---
id: OPTICAL_SCALE_INLINE_MONO
title: "Optical Scaling for Inline Monospace."
essence: "Scale inline monospace down slightly so it blends with proportional prose instead of dominating it."
---

When monospace tokens (`<code>`, inline literals) appear inside proportional body text, they read optically heavier at the same px size: monospace glyphs consume 20–30% more horizontal space and carry more visual weight. Set inline mono at ~0.9em of its parent so it integrates with the prose rhythm rather than punching through it.

Block code (`<pre>`) is exempt; it lives in its own typographic context and should match its container's base size.

This correction is applied by every mature prose type system (GitHub Primer at 85%, Bootstrap, Tailwind Typography). Without it, tokens like `Prop` or `implies_intro` visibly dominate surrounding sentences and flatten the hierarchy between content and inline references.
