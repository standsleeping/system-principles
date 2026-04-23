---
id: ADJACENT_SHADE_SEPARATION
title: "Adjacent Shade Separation."
essence: "When two surfaces of different shade meet without strong value contrast, draw a border at the boundary; the eye cannot parse soft adjacent values on its own."
tags: [color, borders, surfaces]
related: [FLAT_VISUAL_HIERARCHY, BOUNDARY_OWNERSHIP, ONE_SIGNAL_PER_MEANING, COLOR_USAGE]
---

Two surfaces of similar value (gray-50 next to gray-100, white next to a hovered row's tint, a muted section against its page background) do not resolve into distinct regions on their own. The eye reads a muddy transition rather than an edge. This is the color-interaction problem Josef Albers documented: boundaries between similar values require explicit definition.

The fix is a thin border at the boundary, a shade darker than either surface. A single pixel is enough; the role is edge definition, not decoration.

## Where it applies

1. **Hover and selection states.** A hovered row whose background differs from the page by one value step needs a boundary on every side where those two shades meet, not just the sides that happen to carry row separators.
2. **Tinted regions on a neutral page.** A subtly-tinted panel (alert strip, callout, summary block) whose fill sits close to the page's value needs a border to resolve its edges; alternatively, deepen the value step.
3. **Disabled or muted sections.** A section rendered in a slightly different shade to indicate inactivity still needs an edge; the shade change alone will not read.
4. **Cards against a panel.** When a card's background is close in value to its container, the card's edge dissolves without a border.

Inline exceptions exist at small scale: inline `<code>` uses a shaded background against prose, and the subtle value difference reads because the glyphs are small and the inline rhythm carries the eye. Block-level surfaces do not have this luxury.

## The test

Squint at the surface boundary. If the two regions still read as distinct, the contrast is sufficient and no border is needed. If the edge dissolves, either deepen the value step or add a border.

## Relation to adjacent principles

- **FLAT_VISUAL_HIERARCHY** flattens nested boxes to one surface with border separators. The adjacent-shade rule is the mechanism for drawing those separators: it names *when* one is earned.
- **BOUNDARY_OWNERSHIP** answers *which* component should draw a given border. This principle answers *whether* one is needed at all.
- **ONE_SIGNAL_PER_MEANING** is not violated by the border; the border defines an edge (structure), while the shade carries meaning (state). Two signals, two purposes.
