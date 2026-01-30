---
id: ONE_SIGNAL_PER_MEANING
title: "One Signal Per Meaning."
summary: "Each piece of information should be communicated once, through one visual channel."
---

Each piece of information should be communicated once, through one visual channel.

When the same meaning is conveyed through multiple signals, it creates redundancy. The user sees two visual changes but learns one fact. The extra signal is noise.

Choose one visual channel per meaning:

| Meaning | Preferred Signal | Avoid Adding |
|---------|------------------|--------------|
| Navigable/clickable | Text color (blue) | Background color |
| Selected | Background color | Border + background |
| Disabled | Opacity reduction | Gray text + gray background |
| Error state | Text color (red) | Red text + red border + red background |

Multiple signals are appropriate when they serve different purposes: accessibility (focus states may use both outline AND background), different information (blue text for navigable + badge for count convey different facts).

Test for redundancy: "If I remove this visual treatment, does the user lose information?" If no, remove it.