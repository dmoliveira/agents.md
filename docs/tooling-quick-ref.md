# Tooling Quick Reference

Use this page for command discovery. Policy lives in `AGENTS.md`; detailed procedures live in the linked workflow docs.

## Start and track

```bash
make help
git fetch --all --prune
gh pr status
oc current
oc next --scope <repo-scope> --limit 5
oc queue --scope <repo-scope> --limit 10
```

- Read-only work may skip tracking and remote checks.
- Implementation/delivery follows `docs/codememory-workflow.md` and uses a dedicated worktree.
- Resume a known slice with `oc resume --scope <repo-scope> --task <task_id>`.
- Create/close tracked work with `oc add task ...`, `oc add session ... --worktree . --task <task_id>`, `oc done ...`, and `oc end-session ...`.

## Local validation

```bash
git diff --check
make wiki-sync-check  # only for mirror-controlled docs
make preflight        # authenticated remote-readiness check
```

Use `make help` for the complete, repository-confirmed target list. Do not assume targets from another repository exist here.

For Python projects:

```bash
python3 -m py_compile <touched-files>
uv run ruff check .
uv run pytest -q
```

For live-state behavior, use the iterative-testing module and `tmux` when static checks are insufficient.

## Search and delivery

```bash
rg -n "pattern" -g "*.md"
fd -e md
gh pr view <id>
gh pr checks <id>
```

Run PR/merge/cleanup commands only in the Delivery/e2e lane. See `docs/github-cli.md` and `docs/orchestration-advanced.md`.

## Optional tools

- Browser automation is for UI-owned OAuth, install, re-auth, scope, or final-visual blockers; use shell first. See `docs/agent-browser.md`.
- OpenCode image/concise commands are optional when `my_opencode` is available: `/image access --json`, `/image preference show --json`, `/image location show --json`, `/gateway concise status`.
- Keep commands non-interactive and CI-safe.

## References

- `docs/codememory-workflow.md` — tracking, recovery, handoff, and closeout.
- `docs/codememory-conventions.md` — Codememory taxonomy and repo defaults.
- `docs/validation-policy.md` — checks, risk, review budgets, and exit criteria.
- `docs/iterative-testing-workflow.md` — live-state and sandbox validation.
- `docs/concise-communication-workflow.md` — concise communication behavior.
- `docs/agent-browser.md` — browser-only blockers.
