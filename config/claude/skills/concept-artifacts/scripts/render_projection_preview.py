"""Render projection matrix artifacts as a static preview page.

Usage: python render_projection_preview.py <concepts_dir_or_projection_matrices_dir> [output_html]
"""

import argparse
import json
import sys
from collections import Counter
from html import escape
from pathlib import Path

STATUSES = ("projected", "excluded", "missing", "not-applicable")


def load_json(path: Path) -> dict[str, object]:
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def as_str(val: object) -> str:
    if not isinstance(val, str):
        raise TypeError(f"Expected str, got {type(val).__name__}")
    return val


def as_list(val: object) -> list[object]:
    if not isinstance(val, list):
        raise TypeError(f"Expected list, got {type(val).__name__}")
    return list(val)


def as_dict(val: object) -> dict[str, object]:
    if not isinstance(val, dict):
        raise TypeError(f"Expected dict, got {type(val).__name__}")
    return {str(k): v for k, v in val.items()}


def projection_matrix_dir(path: Path) -> Path:
    """Accept either concepts/ or projection-matrices/ as input."""
    if path.is_file():
        return path.parent
    nested = path / "projection-matrices"
    return nested if nested.is_dir() else path


def load_projection_matrices(path: Path) -> list[dict[str, object]]:
    """Load every projection matrix JSON artifact from a file or directory."""
    if path.is_file():
        paths = [path]
    else:
        paths = sorted(projection_matrix_dir(path).glob("*.json"))

    matrices: list[dict[str, object]] = []
    for matrix_path in paths:
        matrix = load_json(matrix_path)
        if matrix.get("$schema") == "projection-matrix.schema.json":
            matrices.append(matrix)

    if not matrices:
        raise ValueError(f"No projection matrices found in {path}")
    return sorted(matrices, key=lambda m: as_str(m["concept"]).lower())


def default_output_path(input_path: Path) -> Path:
    if input_path.is_file():
        return input_path.with_suffix(".html")
    if (input_path / "projection-matrices").is_dir():
        return input_path / "projection-preview.html"
    return projection_matrix_dir(input_path).parent / "projection-preview.html"


def status_counts(matrices: list[dict[str, object]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for matrix in matrices:
        for row_kind in ("actions", "emissions"):
            for row_obj in as_list(matrix.get(row_kind, [])):
                row = as_dict(row_obj)
                for cell_obj in as_list(row["cells"]):
                    cell = as_dict(cell_obj)
                    counts[as_str(cell["status"])] += 1
    return counts


def row_count(matrices: list[dict[str, object]], row_kind: str) -> int:
    return sum(len(as_list(matrix.get(row_kind, []))) for matrix in matrices)


def cell_text(cell: dict[str, object]) -> str:
    status = as_str(cell["status"])
    if status == "projected":
        element = as_str(cell.get("element", ""))
        label = as_str(cell.get("label", ""))
        return f"{element}: {label}" if element else label
    if status == "excluded":
        return as_str(cell.get("reason", "Excluded"))
    if status == "missing":
        return "Missing"
    if status == "not-applicable":
        return "Not applicable"
    return status


def cell_title(cell: dict[str, object]) -> str:
    parts: list[str] = []
    for key in ("source", "expected_from", "reason"):
        value = cell.get(key)
        if isinstance(value, str):
            parts.append(f"{key}: {value}")
    return " | ".join(parts)


def render_channel_heading(channel: dict[str, object]) -> str:
    key = escape(as_str(channel["key"]))
    meta_parts = [
        as_str(channel[field])
        for field in ("direction", "sync", "transport", "encoding", "surface")
        if isinstance(channel.get(field), str)
    ]
    meta = " / ".join(meta_parts)
    return (
        f'<div class="channel-key">{key}</div>'
        f'<div class="channel-meta">{escape(meta)}</div>'
    )


def render_cell(cell: dict[str, object]) -> str:
    status = as_str(cell["status"])
    status_class = status.replace("-", "_")
    title = cell_title(cell)
    title_attr = f' title="{escape(title)}"' if title else ""
    return (
        f'<td class="matrix-cell status-{status_class}"{title_attr}>'
        f'<span class="status-label">{escape(status.replace("-", " "))}</span>'
        f'<span class="cell-text">{escape(cell_text(cell))}</span>'
        "</td>"
    )


def render_rows(
    *,
    kind: str,
    rows: list[object],
    channel_keys: list[str],
    colspan: int,
) -> str:
    parts = [
        f'<tr class="matrix-kind"><th colspan="{colspan}">{escape(kind)}</th></tr>'
    ]
    if not rows:
        parts.append(
            f'<tr><th class="target-name" colspan="{colspan}">No {escape(kind.lower())}</th></tr>'
        )
        return "\n".join(parts)

    for row_obj in rows:
        row = as_dict(row_obj)
        cells_by_channel = {
            as_str(as_dict(cell)["channel"]): as_dict(cell)
            for cell in as_list(row["cells"])
        }
        parts.append("<tr>")
        parts.append(f'<th class="target-name">{escape(as_str(row["name"]))}</th>')
        for channel in channel_keys:
            cell = cells_by_channel.get(channel)
            if cell is None:
                parts.append('<td class="matrix-cell status-unknown">-</td>')
            else:
                parts.append(render_cell(cell))
        parts.append("</tr>")
    return "\n".join(parts)


def render_matrix(matrix: dict[str, object]) -> str:
    channels = [as_dict(c) for c in as_list(matrix["channels"])]
    channel_keys = [as_str(c["key"]) for c in channels]
    colspan = len(channel_keys) + 1
    concept = as_str(matrix["concept"])

    parts = [
        '<section class="concept-section">',
        f"<h2>{escape(concept)}</h2>",
        '<div class="matrix-wrap">',
        '<table class="projection-matrix">',
        "<thead>",
        "<tr>",
        '<th class="target-heading">Target</th>',
    ]
    for channel in channels:
        parts.append(f"<th>{render_channel_heading(channel)}</th>")
    parts.extend(
        [
            "</tr>",
            "</thead>",
            "<tbody>",
            render_rows(
                kind="Actions",
                rows=as_list(matrix.get("actions", [])),
                channel_keys=channel_keys,
                colspan=colspan,
            ),
            render_rows(
                kind="Emissions",
                rows=as_list(matrix.get("emissions", [])),
                channel_keys=channel_keys,
                colspan=colspan,
            ),
            "</tbody>",
            "</table>",
            "</div>",
            "</section>",
        ]
    )
    return "\n".join(parts)


def render_preview_html(matrices: list[dict[str, object]]) -> str:
    counts = status_counts(matrices)
    summary_items = [
        ("Concepts", str(len(matrices))),
        ("Actions", str(row_count(matrices, "actions"))),
        ("Emissions", str(row_count(matrices, "emissions"))),
        *[
            (status.replace("-", " ").title(), str(counts.get(status, 0)))
            for status in STATUSES
        ],
    ]
    summary = "\n".join(
        f'<div class="metric"><span>{escape(label)}</span><strong>{escape(value)}</strong></div>'
        for label, value in summary_items
    )
    matrices_html = "\n".join(render_matrix(matrix) for matrix in matrices)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projection Matrix Preview</title>
<style>
/* DK-inspired: gray-dominant, purple accent, monospace chrome, square corners,
   thin borders, no shadows. Self-contained (system fonts, no embedded assets). */
:root {{
  color-scheme: light dark;
  --bg: light-dark(#f5f5f5, #181619);
  --surface: light-dark(#ffffff, #1e1c1f);
  --subtle: light-dark(#ececed, #232027);
  --text: light-dark(#181619, #ececed);
  --muted: light-dark(#57545a, #9f9ca2);
  --border: light-dark(#c5c3c7, #363438);
  --accent: light-dark(#8300ca, #bf80ff);
  --ok: light-dark(#3c5f00, #8fd900);
  --danger: light-dark(#bf0000, #ff8080);
  --selection: light-dark(#f1e8ff, #530082);
  --font-mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  --font-prose: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --space-sm: 0.25rem;
  --space-md: 0.5rem;
  --space-lg: 0.75rem;
  --space-xl: 1rem;
  --space-2xl: 1.5rem;
  --border-w: 1px;
  --rail-w: 3px;
  --tracking-wide: 0.04em;
  font-family: var(--font-mono);
}}
* {{ box-sizing: border-box; }}
::selection {{ background: var(--selection); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-size: 0.875rem;
  line-height: 1.5;
}}
header {{
  background: var(--surface);
  border-bottom: var(--border-w) solid var(--border);
  padding: var(--space-lg);
}}
h1, h2 {{ margin: 0; font-weight: 600; }}
h1 {{ font-size: 1.5rem; }}
h2 {{ font-size: 1.125rem; }}
main {{
  display: flex;
  flex-direction: column;
  gap: var(--space-2xl);
  padding: var(--space-2xl);
}}
.summary {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(8rem, 1fr));
  background: var(--surface);
  border-bottom: var(--border-w) solid var(--border);
}}
.metric {{
  padding: var(--space-lg);
  border-right: var(--border-w) solid var(--border);
}}
.metric span {{
  display: block;
  color: var(--muted);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
}}
.metric strong {{
  display: block;
  margin-top: var(--space-sm);
  font-size: 1.5rem;
  font-weight: 600;
}}
.concept-section {{
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}}
.matrix-wrap {{
  overflow: auto;
  border: var(--border-w) solid var(--border);
  background: var(--surface);
}}
.projection-matrix {{
  width: 100%;
  min-width: 48rem;
  border-collapse: collapse;
  table-layout: fixed;
}}
th, td {{
  border: var(--border-w) solid var(--border);
  padding: var(--space-md);
  vertical-align: top;
  text-align: left;
}}
thead th {{ background: var(--surface); }}
.target-heading, .target-name {{ width: 13.75rem; }}
.target-name {{ font-weight: 600; background: var(--subtle); }}
.matrix-kind th {{
  color: var(--muted);
  background: var(--subtle);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  font-size: 0.75rem;
  font-weight: 600;
}}
.channel-key {{ font-weight: 600; }}
.channel-meta {{
  margin-top: var(--space-sm);
  color: var(--muted);
  font-size: 0.6875rem;
  overflow-wrap: anywhere;
}}
.matrix-cell {{ position: relative; overflow-wrap: anywhere; }}
.status-label {{
  display: block;
  margin-bottom: var(--space-sm);
  color: var(--muted);
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
}}
.cell-text {{ font-family: var(--font-prose); color: var(--text); }}
/* Status as a thin left rail + label tint, not a full-cell wash. */
.status-projected::before,
.status-missing::before {{
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--rail-w);
}}
.status-projected::before {{ background: var(--ok); }}
.status-missing::before {{ background: var(--danger); }}
.status-missing .status-label {{ color: var(--danger); }}
.status-unknown {{ color: var(--muted); }}
</style>
</head>
<body>
<header>
  <h1>Projection Matrix Preview</h1>
</header>
<section class="summary" aria-label="Summary">
{summary}
</section>
<main>
{matrices_html}
</main>
</body>
</html>
"""


def write_projection_preview(input_path: Path, output_path: Path | None = None) -> Path:
    matrices = load_projection_matrices(input_path)
    destination = output_path or default_output_path(input_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_preview_html(matrices), encoding="utf-8")
    return destination


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render projection matrices as a static preview HTML page.",
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to concepts/, projection-matrices/, or one matrix JSON file.",
    )
    parser.add_argument(
        "output_html",
        nargs="?",
        type=Path,
        help="Output HTML path (default: projection-preview.html beside the inputs).",
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    parsed = parse_args(args)
    output = write_projection_preview(
        parsed.input_path.resolve(),
        parsed.output_html.resolve() if parsed.output_html is not None else None,
    )
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
