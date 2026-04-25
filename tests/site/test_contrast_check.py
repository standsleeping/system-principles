"""Tests for the contrast-check audit."""

import pytest

from principles.site.contrast_check import (
    Pair,
    audit,
    contrast_ratio,
    parse_tokens,
    relative_luminance,
    resolve,
)


# === parse_tokens ===


def test_parse_tokens_extracts_basic_definitions() -> None:
    """Collects --name: value; pairs into a flat map."""
    css = ":root { --color-a: #ffffff; --color-b: #000000; }"
    assert parse_tokens(css) == {"color-a": "#ffffff", "color-b": "#000000"}


def test_parse_tokens_keeps_light_dark_expression_intact() -> None:
    """Stores the raw value so resolve() can interpret light-dark() branches."""
    css = "--color-bg: light-dark(var(--gray-50), var(--gray-700));"
    tokens = parse_tokens(css)
    assert tokens["color-bg"] == "light-dark(var(--gray-50), var(--gray-700))"


# === resolve ===


def test_resolve_picks_light_branch() -> None:
    """In light theme, the first arg of light-dark() is returned."""
    tokens = {
        "color-bg": "light-dark(var(--gray-50), var(--gray-700))",
        "gray-50": "#F5F5F5",
        "gray-700": "#181619",
    }
    assert resolve("color-bg", "light", tokens) == "#F5F5F5"


def test_resolve_picks_dark_branch() -> None:
    """In dark theme, the second arg of light-dark() is returned."""
    tokens = {
        "color-bg": "light-dark(var(--gray-50), var(--gray-700))",
        "gray-50": "#F5F5F5",
        "gray-700": "#181619",
    }
    assert resolve("color-bg", "dark", tokens) == "#181619"


def test_resolve_follows_direct_hex() -> None:
    """A token defined as a literal hex value resolves to itself in any theme."""
    tokens = {"color-fixed": "#C0FFEE"}
    assert resolve("color-fixed", "light", tokens) == "#C0FFEE"
    assert resolve("color-fixed", "dark", tokens) == "#C0FFEE"


def test_resolve_raises_on_unknown_token() -> None:
    """Unknown tokens raise ValueError rather than silently returning a default."""
    with pytest.raises(ValueError, match="unknown token"):
        resolve("color-missing", "light", {})


def test_resolve_raises_on_non_hex_leaf() -> None:
    """A token that resolves to a non-hex value (rgb(), named color) is an error."""
    tokens = {"color-weird": "rgb(0, 0, 0)"}
    with pytest.raises(ValueError, match="non-hex"):
        resolve("color-weird", "light", tokens)


# === WCAG contrast ===


def test_contrast_white_on_black_is_21_to_1() -> None:
    """The theoretical maximum — pure white on pure black."""
    assert contrast_ratio("#ffffff", "#000000") == pytest.approx(21.0, abs=0.01)


def test_contrast_identical_colors_is_1_to_1() -> None:
    """Two identical colors have the minimum possible ratio (no contrast)."""
    assert contrast_ratio("#808080", "#808080") == pytest.approx(1.0, abs=0.001)


def test_contrast_is_symmetric() -> None:
    """Order of arguments does not change the ratio."""
    a, b = "#F5F5F5", "#181619"
    assert contrast_ratio(a, b) == pytest.approx(contrast_ratio(b, a), rel=1e-6)


def test_relative_luminance_white_is_1() -> None:
    """Pure white has luminance 1.0 by definition."""
    assert relative_luminance("#ffffff") == pytest.approx(1.0, abs=1e-6)


def test_relative_luminance_black_is_0() -> None:
    """Pure black has luminance 0.0."""
    assert relative_luminance("#000000") == pytest.approx(0.0, abs=1e-6)


# === end-to-end: integration on an actual palette fragment ===


def test_resolve_and_contrast_together() -> None:
    """Verifies the pipeline: parse CSS → resolve per theme → compute contrast."""
    css = """
    :root {
      --color-bg: light-dark(var(--gray-50), var(--gray-700));
      --color-text: light-dark(var(--gray-700), var(--gray-50));
      --gray-50: #F5F5F5;
      --gray-700: #181619;
    }
    """
    tokens = parse_tokens(css)
    light_bg = resolve("color-bg", "light", tokens)
    light_text = resolve("color-text", "light", tokens)
    assert light_bg == "#F5F5F5"
    assert light_text == "#181619"
    assert contrast_ratio(light_bg, light_text) > 15  # well above AA readable


# === audit ===


def test_audit_flags_colliding_pair() -> None:
    """A declared pair whose tokens collapse to the same value is reported FAIL."""
    css = ":root { --color-a: #808080; --color-b: #808080; }"
    pair = Pair("color-a", "color-b", min_ratio=1.5, reason="synthetic collision")
    results = audit(css, pairs=(pair,))
    assert len(results) == 2  # two themes
    assert all(not r.passed for r in results)
    assert all(r.ratio == pytest.approx(1.0) for r in results)


def test_audit_passes_well_separated_pair() -> None:
    """A declared pair with maximum contrast passes in every theme."""
    css = ":root { --color-a: #000000; --color-b: #FFFFFF; }"
    pair = Pair("color-a", "color-b", min_ratio=4.5, reason="synthetic max contrast")
    results = audit(css, pairs=(pair,))
    assert all(r.passed for r in results)


def test_audit_passes_on_current_palette() -> None:
    """The live palette satisfies every declared contrast contract in both themes."""
    failures = [r for r in audit() if not r.passed]
    assert failures == [], "\n".join(
        f"--{f.pair.a} × --{f.pair.b} ({f.theme}): "
        f"{f.ratio:.2f} < {f.pair.min_ratio} — {f.pair.reason}"
        for f in failures
    )
