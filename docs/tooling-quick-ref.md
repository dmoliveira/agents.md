# Tooling Quick Reference

Use this as a fast productivity map for local utility tools.

## Tool source paths
- Primary: `../my_utils`
- Fallback: `../utils-scripts`
- If neither exists, continue with repo-native commands and existing project tooling.

## High-value tools
- `br` (task flow): `br ready`, `br show <id>`, `br update <id> --status in_progress`, `br close <id>`
- `gh` (PR flow): `gh pr status`, `gh pr create --fill`, `gh pr checks --watch`, `gh pr merge <id> --merge --delete-branch`
- `rg` + `fd` (code search): `fd -e md`, `rg -n "pattern" -g "*.md"`
- `uv` (Python): `uv venv .venv`, `uv run pytest -q`, `uv run ruff check .`
- `make` (entrypoint): `make help`, then run project targets instead of ad-hoc scripts.

## Parallel execution default
- Prefer `parallel` for independent repeated commands instead of `for` loops.
- Base pattern: `parallel --jobs <n> --halt soon,fail=1 '<cmd {1}>' ::: <arg1> <arg2> <arg3>`
- Use when commands are independent and order does not matter.
- Fallback when `parallel` is unavailable: `xargs -P <n>`; use sequential execution when steps are dependent.

### Parallel quick recipes
- Run checks in multiple dirs: `parallel --jobs 3 --halt soon,fail=1 'make -C {} test' ::: pkg-a pkg-b pkg-c`
- Run same command on many files: `parallel --jobs 4 --halt soon,fail=1 'ruff check {}' ::: $(fd -e py)`
- Matrix args (paired lists): `parallel --jobs 4 --halt soon,fail=1 'pytest -q {1} --maxfail={2}' ::: tests/a tests/b :::+ 1 2`
- Dry-run first (safe preview): `parallel --dry-run --jobs 4 'ruff check {}' ::: $(fd -e py)`

## Notes
- Keep commands non-interactive and CI-safe.
- Prefer existing repo conventions over generic defaults when they conflict.
