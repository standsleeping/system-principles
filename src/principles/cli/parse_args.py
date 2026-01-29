"""Command-line argument parsing with subcommands."""

import argparse

from principles.logging import get_logger
from principles.types import Phase

logger = get_logger(__name__)


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments with subcommands."""
    logger.debug("Parsing command line arguments")

    parser = argparse.ArgumentParser(
        prog="principles",
        description="Manage and apply system design principles",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)",
    )

    parser.add_argument(
        "--content-dir",
        default="content",
        help="Path to content directory (default: content)",
    )

    parser.add_argument(
        "--sets-dir",
        default="sets",
        help="Path to sets directory (default: sets)",
    )

    subparsers = parser.add_subparsers(dest="command")

    # principles list
    list_parser = subparsers.add_parser("list", help="List principles")
    list_parser.add_argument(
        "--phase",
        choices=[p.value for p in Phase],
        help="Filter by phase",
    )
    list_parser.add_argument(
        "--category",
        help="Filter by category code (e.g., BD, TD)",
    )
    list_parser.add_argument(
        "--set",
        dest="set_name",
        help="Filter by set name",
    )

    # principles show <id>
    show_parser = subparsers.add_parser("show", help="Show principle details")
    show_parser.add_argument("id", help="Principle ID (e.g., BD1)")

    # principles compile
    compile_parser = subparsers.add_parser("compile", help="Compile principles")
    compile_parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "agent-skill"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    compile_parser.add_argument(
        "--set",
        dest="set_name",
        help="Set name to compile (compiles all if not specified)",
    )
    compile_parser.add_argument(
        "--output",
        "-o",
        help="Output file path (prints to stdout if not specified)",
    )

    return parser.parse_args(args)
