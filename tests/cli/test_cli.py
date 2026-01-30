"""Tests for the command-line interface."""

from principles.cli import parse_args


def test_parse_args_defaults() -> None:
    """Parses with default values."""
    args = parse_args([])
    assert args.log_level == "INFO"
    assert args.content_dir == "content"
    assert args.sets_dir == "sets"
    assert args.taxonomies_dir == "taxonomies"
    assert args.command is None


def test_parse_args_log_level() -> None:
    """Parses log level argument."""
    args = parse_args(["--log-level", "DEBUG"])
    assert args.log_level == "DEBUG"


def test_parse_args_list_command() -> None:
    """Parses list subcommand."""
    args = parse_args(["list"])
    assert args.command == "list"
    assert args.taxonomy == "default"
    assert args.group is None
    assert args.flat is False


def test_parse_args_list_with_taxonomy() -> None:
    """Parses list with taxonomy filter."""
    args = parse_args(["list", "--taxonomy", "custom", "--group", "designing/abstraction"])
    assert args.command == "list"
    assert args.taxonomy == "custom"
    assert args.group == "designing/abstraction"


def test_parse_args_list_flat() -> None:
    """Parses list with flat flag."""
    args = parse_args(["list", "--flat"])
    assert args.command == "list"
    assert args.flat is True


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


def test_parse_args_compile_with_taxonomy() -> None:
    """Parses compile with taxonomy."""
    args = parse_args(["compile", "--taxonomy", "default", "--group", "modeling"])
    assert args.command == "compile"
    assert args.taxonomy == "default"
    assert args.group == "modeling"
