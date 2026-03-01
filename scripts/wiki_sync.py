#!/usr/bin/env python3
"""Sync wiki mirror content to GitHub wiki repository (dry-run/apply)."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile


def run(
    cmd: list[str], cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=True,
    )


def wiki_remote_available(repo: str) -> bool:
    probe = run(
        ["git", "ls-remote", f"https://github.com/{repo}.wiki.git", "HEAD"], check=False
    )
    return probe.returncode == 0


def write_home(tmp_dir: Path, content: str) -> None:
    (tmp_dir / "Home.md").write_text(content, encoding="utf-8")


def commit_if_needed(tmp_dir: Path, message: str) -> bool:
    run(["git", "add", "Home.md"], cwd=tmp_dir)
    status = run(["git", "status", "--porcelain"], cwd=tmp_dir)
    if not status.stdout.strip():
        return False
    run(["git", "commit", "-m", message], cwd=tmp_dir)
    return True


def sync(repo: str, apply: bool) -> int:
    root = Path(__file__).resolve().parents[1]
    mirror_path = root / "docs" / "wiki-home-mirror.md"
    if not mirror_path.exists():
        print("wiki-sync: missing docs/wiki-home-mirror.md")
        return 1

    content = mirror_path.read_text(encoding="utf-8")
    available = wiki_remote_available(repo)
    mode = "apply" if apply else "dry-run"
    print(f"wiki-sync: mode={mode}")
    print(f"wiki-sync: repo={repo}")
    print(f"wiki-sync: remote_ready={str(available).lower()}")

    if not available:
        print(
            "wiki-sync: wiki remote unavailable; keep using docs/wiki-home-mirror.md fallback"
        )
        return 0 if not apply else 1

    with tempfile.TemporaryDirectory(prefix="agents-wiki-sync-") as tmp:
        tmp_dir = Path(tmp)
        clone = run(
            ["git", "clone", f"https://github.com/{repo}.wiki.git", str(tmp_dir)],
            check=False,
        )
        if clone.returncode != 0:
            print("wiki-sync: clone failed")
            print(clone.stderr.strip())
            return 1

        write_home(tmp_dir, content)

        if not apply:
            diff = run(["git", "diff", "--", "Home.md"], cwd=tmp_dir, check=False)
            if diff.stdout.strip():
                print("wiki-sync: dry-run detected pending Home.md changes")
            else:
                print("wiki-sync: dry-run no Home.md changes detected")
            return 0

        changed = commit_if_needed(
            tmp_dir, "Update wiki Home from docs/wiki-home-mirror.md"
        )
        if not changed:
            print("wiki-sync: no changes to push")
            return 0

        push = run(["git", "push", "origin", "HEAD"], cwd=tmp_dir, check=False)
        if push.returncode != 0:
            print("wiki-sync: push failed")
            print(push.stderr.strip())
            return 1
        print("wiki-sync: pushed Home.md to wiki remote")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync wiki mirror into GitHub Wiki Home page"
    )
    parser.add_argument(
        "--repo",
        default="dmoliveira/agents.md",
        help="GitHub repository slug owner/name",
    )
    parser.add_argument(
        "--apply", action="store_true", help="Apply changes to wiki remote"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return sync(args.repo, apply=args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
