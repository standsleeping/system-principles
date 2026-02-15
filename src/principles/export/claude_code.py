"""Claude Code compile specs — which principle groups produce which output files."""

from principles.types import CompileSpec

# The 4 compile specs: which taxonomy groups compile into which output files.
# design-thinking is a fragment (always loaded); the rest are rules (path-matched).
COMPILE_SPECS = (
    CompileSpec(
        groups=("process", "conceptual", "modeling", "structure"),
        output_path="fragments/design-thinking.md",
        header=(
            "# Design Principles\n"
            "\n"
            "Apply these principles when designing and implementing code. "
            "Use the principle ID (e.g., SEPARATE_DECISIONS_BEHAVIOR) when "
            "referencing a decision. For full detail on any principle, use "
            "the `/principles` skill or read the source files in the "
            "system-principles `content/` directory."
        ),
    ),
    CompileSpec(
        groups=("types", "constructs"),
        output_path="rules/python.md",
        header=(
            "# Python Conventions\n"
            "\n"
            "Follow these principles when writing or modifying Python code."
        ),
        paths_frontmatter=("**/*.py",),
    ),
    CompileSpec(
        groups=("testing",),
        output_path="rules/testing.md",
        header=(
            "# Testing Conventions\n"
            "\n"
            "Follow these principles when writing or modifying tests."
        ),
        paths_frontmatter=("**/tests/**", "**/test_*"),
    ),
    CompileSpec(
        groups=("layout", "visual-design", "ui-debugging"),
        output_path="rules/frontend.md",
        header=(
            "# Frontend Conventions\n"
            "\n"
            "Follow these principles when writing or modifying HTML, CSS, or JavaScript."
        ),
        paths_frontmatter=("**/*.html", "**/*.css", "**/*.js"),
    ),
)
