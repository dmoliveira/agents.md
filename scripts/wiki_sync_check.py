#!/usr/bin/env python3
"""Validate alignment between wiki snippet and wiki mirror docs."""

from __future__ import annotations

from pathlib import Path
import sys


REQUIRED_SNIPPET = [
    "- Start here: [README](https://github.com/dmoliveira/agents.md)",
    "- Operating contract: [AGENTS.md](https://github.com/dmoliveira/agents.md/blob/main/AGENTS.md)",
    "- Tooling quick reference: [docs/tooling-quick-ref.md](https://github.com/dmoliveira/agents.md/blob/main/docs/tooling-quick-ref.md)",
    "- Advanced orchestration: [docs/orchestration-advanced.md](https://github.com/dmoliveira/agents.md/blob/main/docs/orchestration-advanced.md)",
    "- Support this work: [docs/support-the-project.md](https://github.com/dmoliveira/agents.md/blob/main/docs/support-the-project.md)",
    "- Use dedicated worktrees per task.",
    "- Keep commits small and focused.",
    "- End cycles with `<CONTINUE-LOOP>` when tasks remain.",
]

REQUIRED_MIRROR = [
    "- Start here: [README](../README.md)",
    "- Operating contract: [AGENTS.md](../AGENTS.md)",
    "- Tooling quick reference: [docs/tooling-quick-ref.md](tooling-quick-ref.md)",
    "- Advanced orchestration: [docs/orchestration-advanced.md](orchestration-advanced.md)",
    "- Support this work: [docs/support-the-project.md](support-the-project.md)",
    "- Use dedicated worktrees per task.",
    "- Keep commits small and focused.",
    "- End cycles with `<CONTINUE-LOOP>` when tasks remain.",
]


def missing(content: str, required: list[str]) -> list[str]:
    return [item for item in required if item not in content]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    snippet_path = repo_root / "docs" / "wiki-home-snippet.md"
    mirror_path = repo_root / "docs" / "wiki-home-mirror.md"

    snippet = snippet_path.read_text(encoding="utf-8")
    mirror = mirror_path.read_text(encoding="utf-8")

    snippet_missing = missing(snippet, REQUIRED_SNIPPET)
    mirror_missing = missing(mirror, REQUIRED_MIRROR)

    if not snippet_missing and not mirror_missing:
        print("wiki-sync-check: ok")
        return 0

    if snippet_missing:
        print("wiki-sync-check: missing snippet entries:")
        for item in snippet_missing:
            print(f"  - {item}")

    if mirror_missing:
        print("wiki-sync-check: missing mirror entries:")
        for item in mirror_missing:
            print(f"  - {item}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
