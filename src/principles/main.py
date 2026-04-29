"""Main entry point for the principles CLI."""

import logging
import sys

from principles.cli import parse_args
from principles.cli.commands import (
    run_compile,
    run_export,
    run_list,
    run_show,
    run_site,
    run_validate,
)
from principles.logging import configure_logging, get_logger

logger = get_logger(__name__)


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)

    log_level = getattr(logging, parsed_args.log_level)
    configure_logging(level=log_level)

    logger.debug(f"Arguments: {parsed_args}")

    command = parsed_args.command

    if command is None:
        # No subcommand given, show usage hint
        print("Usage: principles <command> [options]")
        print("Commands: list, show, compile, export, site, validate")
        print("Use 'principles --help' for more information.")
        return 0

    try:
        if command == "list":
            return run_list(parsed_args)
        elif command == "show":
            return run_show(parsed_args)
        elif command == "compile":
            return run_compile(parsed_args)
        elif command == "export":
            return run_export(parsed_args)
        elif command == "site":
            return run_site(parsed_args)
        elif command == "validate":
            return run_validate(parsed_args)
        else:
            print(f"Unknown command: {command}")
            return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
