"""Site command: build and serve the static principles site."""

import argparse
from pathlib import Path

from principles.site.builder import build_site
from principles.site.server import serve_site


def run_site(args: argparse.Namespace) -> int:
    """Execute the site command."""
    content_dir = Path(args.content_dir)
    taxonomies_dir = Path(args.taxonomies_dir)
    output_dir = Path(args.output_dir)
    taxonomy_name = args.taxonomy

    site_command = args.site_command

    if site_command == "build":
        return build_site(content_dir, taxonomies_dir, output_dir, taxonomy_name)

    elif site_command == "serve":
        result = build_site(content_dir, taxonomies_dir, output_dir, taxonomy_name)
        if result != 0:
            return result
        serve_site(output_dir, args.port)
        return 0

    else:
        print("Usage: principles site {build,serve}")
        return 1
