"""Build-time pairwise contrast audit for the site's CSS tokens.

Enforces TOKEN_PAIR_CONTRAST: every pair of semantic tokens that will appear
adjacent in the rendered site must remain visually distinguishable in every
theme. Failures are token-level bugs (the wrong token used for a context, or
two tokens collapsing to the same primitive in one theme).

Outputs a table of pairs x themes with their computed WCAG contrast ratios,
and exits non-zero if any fall below their declared minimum.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Literal

from .styles import CSS

Theme = Literal["light", "dark"]


# =============================================================================
# Token parsing
# =============================================================================


_TOKEN_DEF = re.compile(r"--([\w-]+):\s*(.+?);")
_LIGHT_DARK = re.compile(r"light-dark\(\s*(.+?)\s*,\s*(.+?)\s*\)")
_VAR_REF = re.compile(r"var\(\s*--([\w-]+)\s*\)")
_HEX = re.compile(r"^#[0-9A-Fa-f]{3,8}$")


def parse_tokens(css: str) -> dict[str, str]:
    """Collect --name: value; definitions into a flat map.

    Later definitions win (matches CSS cascade for :root declarations in one
    file); good enough for a single-stylesheet check.
    """
    out: dict[str, str] = {}
    for name, raw_value in _TOKEN_DEF.findall(css):
        out[name] = raw_value.strip()
    return out


def resolve(token: str, theme: Theme, tokens: dict[str, str]) -> str:
    """Resolve a semantic token to a concrete #hex value in the given theme.

    Follows var() chains and picks the light or dark branch of light-dark().
    Raises ValueError if resolution lands outside the palette (non-hex value).
    """
    seen: set[str] = set()
    value = tokens.get(token)
    if value is None:
        raise ValueError(f"unknown token: --{token}")
    while True:
        if token in seen:
            raise ValueError(f"token cycle through --{token}")
        seen.add(token)

        ld = _LIGHT_DARK.fullmatch(value)
        if ld:
            value = ld.group(1 if theme == "light" else 2).strip()

        ref = _VAR_REF.fullmatch(value)
        if ref:
            token = ref.group(1)
            next_value = tokens.get(token)
            if next_value is None:
                raise ValueError(f"unknown ref: --{token}")
            value = next_value.strip()
            continue

        if _HEX.match(value):
            return value

        raise ValueError(f"--{token} resolved to non-hex value: {value!r}")


# =============================================================================
# WCAG contrast
# =============================================================================


def _channel_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (
        int(h[0:2], 16) / 255,
        int(h[2:4], 16) / 255,
        int(h[4:6], 16) / 255,
    )


def relative_luminance(hex_color: str) -> float:
    r, g, b = _hex_to_rgb(hex_color)
    return (
        0.2126 * _channel_to_linear(r)
        + 0.7152 * _channel_to_linear(g)
        + 0.0722 * _channel_to_linear(b)
    )


def contrast_ratio(a: str, b: str) -> float:
    la = relative_luminance(a)
    lb = relative_luminance(b)
    lighter, darker = (la, lb) if la > lb else (lb, la)
    return (lighter + 0.05) / (darker + 0.05)


# =============================================================================
# Pair list — declared adjacencies with minimum contrast floors
# =============================================================================


@dataclass(frozen=True, slots=True)
class Pair:
    a: str
    b: str
    min_ratio: float
    reason: str


# Contract floors, chosen for role, not for what happens to pass today:
#
#   4.5   WCAG AA for normal text (14-17px). Readability requirement.
#   3.0   WCAG AA for large text and non-text UI boundaries (1.4.11).
#   2.0   Major structural divider (section border, heavy rule) — clearly visible.
#   1.5   Clear boundary between two surfaces — distinguishable at a glance.
#   1.3   Minor separator (table row divider) — subtle but readable.
#   1.05  Intentionally subtle tint (hover fill, code-bg). Catches the
#         collapse-to-identical case (ratio 1.0) without demanding prominence.
PAIRS: tuple[Pair, ...] = (
    # --- Text on its background ---
    Pair("color-bg", "color-text", 4.5, "body text"),
    Pair("color-bg", "color-text-muted", 4.5, "muted text"),
    Pair("color-bg", "color-text-subtle", 3.0, "subtle/tertiary text"),
    Pair("color-bg", "color-link", 4.5, "link text"),
    Pair("color-bg", "color-link-hover", 4.5, "link hover"),
    Pair("color-bg", "color-placeholder", 4.5, "placeholder input text"),
    # --- Adjacent-shade separators ---
    Pair("color-bg", "color-border", 1.3, "minor row/cell separator"),
    Pair("color-bg", "color-border-heavy", 2.0, "section/divider heavy rule"),
    Pair("color-bg", "color-hover-bg", 1.05, "hover fill vs page (subtle tint)"),
    Pair("color-bg", "color-code-bg", 1.05, "code fill vs page (subtle tint)"),
    # --- Hover state composition: the regression vector we keep hitting ---
    Pair(
        "color-hover-bg",
        "color-border-heavy",
        1.5,
        "row hover outline vs hover fill",
    ),
    Pair("color-hover-bg", "color-text", 4.5, "text legibility on hover"),
    Pair("color-hover-bg", "color-link", 4.5, "link legibility on hover"),
    # --- Focus-ring-light (selected nav state, ::selection) vs page ---
    Pair(
        "color-bg",
        "color-focus-ring-light",
        1.05,
        "selected row tint vs page (subtle)",
    ),
    # --- Code blocks ---
    Pair("color-code-bg", "color-text", 4.5, "code text on code fill"),
    # --- Focus ring ---
    Pair("color-bg", "color-focus-ring", 3.0, "focus ring visibility (WCAG 1.4.11)"),
)


# =============================================================================
# Reporting
# =============================================================================


@dataclass(frozen=True, slots=True)
class Result:
    pair: Pair
    theme: Theme
    value_a: str
    value_b: str
    ratio: float

    @property
    def passed(self) -> bool:
        return self.ratio >= self.pair.min_ratio


def audit(css: str = CSS, pairs: tuple[Pair, ...] = PAIRS) -> list[Result]:
    tokens = parse_tokens(css)
    results: list[Result] = []
    for pair in pairs:
        for theme in ("light", "dark"):
            va = resolve(pair.a, theme, tokens)
            vb = resolve(pair.b, theme, tokens)
            results.append(
                Result(
                    pair=pair,
                    theme=theme,
                    value_a=va,
                    value_b=vb,
                    ratio=contrast_ratio(va, vb),
                )
            )
    return results


def format_report(results: list[Result]) -> str:
    lines: list[str] = []
    lines.append(
        f"{'PAIR':<50}  {'THEME':<5}  {'A':<8}  {'B':<8}  {'RATIO':>6}  {'MIN':>5}  STATUS"
    )
    lines.append("-" * 100)
    for r in results:
        pair_label = f"--{r.pair.a} x --{r.pair.b}"[:50]
        status = "ok" if r.passed else "FAIL"
        lines.append(
            f"{pair_label:<50}  {r.theme:<5}  {r.value_a:<8}  {r.value_b:<8}  "
            f"{r.ratio:>6.2f}  {r.pair.min_ratio:>5.2f}  {status}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    _ = argv  # unused; here to make the entry point CLI-shaped
    results = audit()
    print(format_report(results))
    failures = [r for r in results if not r.passed]
    print()
    if failures:
        print(f"{len(failures)} pair(s) below their declared minimum:")
        for f in failures:
            print(
                f"  --{f.pair.a} x --{f.pair.b} ({f.theme}): "
                f"{f.ratio:.2f} < {f.pair.min_ratio} — {f.pair.reason}"
            )
        return 1
    print(f"ok: {len(results)} checks passed ({len(PAIRS)} pairs x 2 themes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
