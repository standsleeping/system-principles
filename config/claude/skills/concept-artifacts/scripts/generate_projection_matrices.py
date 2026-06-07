"""Generate derived projection matrix artifacts for concept manifests.

Usage: python generate_projection_matrices.py <concepts_dir> [output_dir]
"""

import argparse
import sys
from pathlib import Path

from validate_concepts import write_projection_matrices


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate derived projection matrix artifacts.",
    )
    parser.add_argument(
        "concepts_dir",
        type=Path,
        help="Path to the concepts directory.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        help="Output directory (default: <concepts_dir>/projection-matrices).",
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    parsed = parse_args(args)
    concepts_dir: Path = parsed.concepts_dir.resolve()
    output_dir: Path | None = (
        parsed.output_dir.resolve() if parsed.output_dir is not None else None
    )

    written = write_projection_matrices(concepts_dir, output_dir)
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
