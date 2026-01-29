"""Core domain types for the principles system."""

from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

# === Domain Identifiers ===

PrincipleId = NewType("PrincipleId", str)
CategoryCode = NewType("CategoryCode", str)
SetName = NewType("SetName", str)
TargetName = NewType("TargetName", str)


# === Enums ===


class Phase(Enum):
    """Development activity phases where principles apply."""

    DESIGNING = "designing"
    MODELING = "modeling"
    STRUCTURING = "structuring"
    IMPLEMENTING = "implementing"
    VERIFYING = "verifying"
    PRESENTING = "presenting"


class OutputFormat(Enum):
    """Supported output formats for compilation."""

    MARKDOWN = "markdown"
    AGENT_SKILL = "agent-skill"
    HTML = "html"


# === Domain Types ===


@dataclass(frozen=True, slots=True)
class Category:
    """A grouping of related principles within a phase."""

    code: CategoryCode
    name: str
    phase: Phase


@dataclass(frozen=True, slots=True)
class Principle:
    """A single design principle with full content."""

    id: PrincipleId
    title: str
    summary: str
    category: Category
    content: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    related: tuple[PrincipleId, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class PrincipleSet:
    """A named collection of principle IDs."""

    name: SetName
    description: str
    principle_ids: tuple[PrincipleId, ...]


@dataclass(frozen=True, slots=True)
class TargetConfig:
    """Configuration for syncing principles to a target project."""

    name: TargetName
    repo: str
    branch: str
    path: str
    output_format: OutputFormat
    sets: tuple[SetName, ...]


# === Error Types (explicit, no exceptions) ===


@dataclass(frozen=True, slots=True)
class ParseError:
    """Error from parsing a file."""

    file_path: str
    message: str
    line: int | None = None


@dataclass(frozen=True, slots=True)
class ValidationError:
    """Error from validating principle data."""

    message: str
    principle_id: PrincipleId | None = None
    field: str | None = None
