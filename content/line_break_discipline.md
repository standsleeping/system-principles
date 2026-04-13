---
id: LINE_BREAK_DISCIPLINE
title: "Line Break Discipline."
essence: "Text wraps at meaningful boundaries without widows, but never at the cost of causing horizontal page scroll."
---

Two failure modes in wrapped text:

1. **Widows** — a single word or character stranded on the last line of a block (e.g., `q` alone at the end of "a Proof p → Proof q"). The break point is technically a valid word boundary, but the result looks broken.
2. **Mid-token breaks in code** — a syntactic expression split across lines in a way that hides its structure (e.g., `Proof p → Proof` / `q`). Code tokens form units; breaking inside a unit obscures meaning.

Both come from the browser's default wrapping algorithm trying to fit text into a narrow container without knowledge of semantic boundaries.

## The constraint that takes precedence

Before applying any fix, remember that `NO_PAGE_SCROLL` wins. A fix that introduces horizontal overflow is worse than the widow it was trying to solve. In particular:

- **`white-space: nowrap` on `<code>` is dangerous.** It forces long code expressions to stay on one line, pushing the container wider than the viewport. Applied globally, it is one of the most common causes of page-level horizontal scroll.
- **Non-breaking glue** (`&nbsp;`, `<span class="nowrap">`) can also overflow if the combined phrase exceeds the container width.

Any nowrap-based solution must be scoped to content whose width you can guarantee fits the smallest container it lives in.

## Fix hierarchy, safest to riskiest

1. **`text-wrap: pretty`** on prose containers (`p`, `li`, `td`). The browser rebalances line breaks to avoid widows automatically. No overflow risk. Graceful fallback in older browsers (they just wrap normally). This should be the default on any prose container.
2. **`text-wrap: balance`** for headings and short labels. Distributes text evenly across lines. No overflow risk because the total width is already bounded by the container.
3. **Restructure the content.** Shorter phrasing, split across logical pieces, or rewritten to avoid the awkward break entirely. No CSS solution needed.
4. **`&nbsp;` for short phrases.** Glue two short words together ("call it" → "call&nbsp;it") when you can verify the combined width fits. Growing the phrase length grows the overflow risk.
5. **`white-space: nowrap`** scoped very narrowly, only when you can prove the content fits. Almost never appropriate on `<code>`; almost never appropriate globally.

## Code that's too wide for its container

The answer is not "prevent wrapping" but "wrap gracefully or scope the scroll":

- **Allow the wrap.** Inline `<code>` should wrap at word boundaries like any other text, even if the break point is aesthetically imperfect. A wrapped code token is better than page overflow.
- **Use `overflow-wrap: break-word`** to ensure very long identifiers break rather than overflow.
- **Promote to a block.** If an expression is long enough that inline wrapping looks bad, put it in a `<pre>` block with `overflow-x: auto`. The scroll is scoped to the block, not the page.

## Summary rule

Apply `text-wrap: pretty` as the default on prose containers. Allow inline code to wrap. If a specific widow or mid-token break still bothers you, fix it by restructuring the content before reaching for nowrap. If you do reach for nowrap, scope it narrowly and verify it can never cause the container to exceed its bounds.
