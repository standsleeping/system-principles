"""Tests for the command-line interface."""

from principles.cli import parse_args


def test_parse_args_defaults() -> None:
    """Parses with default values."""
    args = parse_args([])
    assert args.log_level == "INFO"
    assert args.content_dir == "content"
    assert args.sets_dir == "sets"
    assert args.command is None


def test_parse_args_log_level() -> None:
    """Parses log level argument."""
    args = parse_args(["--log-level", "DEBUG"])
    assert args.log_level == "DEBUG"


def test_parse_args_list_command() -> None:
    """Parses list subcommand."""
    args = parse_args(["list"])
    assert args.command == "list"


def test_parse_args_list_with_phase() -> None:
    """Parses list with phase filter."""
    args = parse_args(["list", "--phase", "designing"])
    assert args.command == "list"
    assert args.phase == "designing"


def test_parse_args_show_command() -> None:
    """Parses show subcommand."""
    args = parse_args(["show", "BD1"])
    assert args.command == "show"
    assert args.id == "BD1"


def test_parse_args_compile_command() -> None:
    """Parses compile subcommand."""
    args = parse_args(["compile", "--format", "agent-skill", "--set", "core"])
    assert args.command == "compile"
    assert args.format == "agent-skill"
    assert args.set_name == "core"
