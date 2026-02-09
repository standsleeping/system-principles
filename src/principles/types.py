"""Core domain types for the principles system."""

from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

# === Domain Identifiers ===

PrincipleId = NewType("PrincipleId", str)
SetName = NewType("SetName", str)
TargetName = NewType("TargetName", str)
TaxonomyName = NewType("TaxonomyName", str)
GroupPath = NewType("GroupPath", str)  # e.g., "designing/abstraction"


# === Enums ===


class OutputFormat(Enum):
    """Supported output formats for compilation."""

    MARKDOWN = "markdown"
    AGENT_SKILL = "agent-skill"
    ESSENCES = "essences"
    HTML = "html"


# === Domain Types ===


@dataclass(frozen=True, slots=True)
class Principle:
    """A single design principle with full content."""

    id: PrincipleId
    title: str
    essence: str
    content: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    related: tuple[PrincipleId, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class TaxonomyGroup:
    """A node in a taxonomy tree that may contain principles or subgroups."""

    name: str
    principle_ids: tuple[PrincipleId, ...] = field(default_factory=tuple)
    subgroups: tuple["TaxonomyGroup", ...] = field(default_factory=tuple)
    description: str = ""

    def get_all_principle_ids(self) -> set[PrincipleId]:
        """Get all principle IDs in this group and its subgroups recursively."""
        result = set(self.principle_ids)
        for subgroup in self.subgroups:
            result.update(subgroup.get_all_principle_ids())
        return result


@dataclass(frozen=True, slots=True)
class Taxonomy:
    """A hierarchical organization of principles."""

    name: TaxonomyName
    description: str
    groups: tuple[TaxonomyGroup, ...]

    def get_all_principle_ids(self) -> set[PrincipleId]:
        """Get all principle IDs in this taxonomy."""
        result: set[PrincipleId] = set()
        for group in self.groups:
            result.update(group.get_all_principle_ids())
        return result

    def get_principles_by_path(self, path: GroupPath) -> set[PrincipleId]:
        """Get all principle IDs under a specific path.

        Path format: "group/subgroup/subsubgroup"
        Example: "designing/abstraction"
        """
        parts = path.split("/")
        current_groups = self.groups

        for part in parts:
            found = None
            for group in current_groups:
                if group.name == part:
                    found = group
                    break
            if found is None:
                return set()
            current_groups = found.subgroups

        # found is now the target group
        if found is not None:
            return found.get_all_principle_ids()
        return set()

    def get_paths_for_principle(self, principle_id: PrincipleId) -> list[str]:
        """Get all paths where a principle appears in this taxonomy."""

        def search(groups: tuple[TaxonomyGroup, ...], prefix: str) -> list[str]:
            paths: list[str] = []
            for group in groups:
                current_path = f"{prefix}/{group.name}" if prefix else group.name
                if principle_id in group.principle_ids:
                    paths.append(current_path)
                paths.extend(search(group.subgroups, current_path))
            return paths

        return search(self.groups, "")


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
