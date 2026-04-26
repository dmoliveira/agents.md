# Validation Policy

Use validation at key gates so iteration stays fast without skipping quality checks.

## Gate policy
- Start gate (required): fetch/check the remote before implementation so the task still matches the latest branch and PR state.
- For iterative or stateful products, prefer validating against the current running state when feasible instead of inferring behavior from files alone.
- Pre-PR gate (required): run the selected validation set once on the full current diff.
- For important or behavior-heavy changes, add one best-available sandbox run that exercises the real flow in isolation before claiming confidence.
- Pre-merge gate (conditional): re-run only when code changed after review or CI reported failures.
- Final remote check (required): compare with latest `main` and overlapping PRs right before merge; update if upstream changes would stale or conflict with the current branch.
- During implementation: run quick smoke checks only when needed to unblock risky debugging.
- For CLI or TUI workflows where current live terminal state is needed to validate or debug behavior, use `tmux` if available to inspect live output, keep the process attached, and send non-interactive commands into the running session.

## Risk matrix
- Docs-only: run `git diff --check`; skip heavier checks unless behavior changed.
- Low-risk code: run targeted lint/test for the touched area plus one smoke path.
- Iterative/stateful flows: add a live smoke path against the running process or session state when that is where failures surface.
- High-risk/runtime/security/migration: run full required lint/test/build suite.
- Important runtime changes: prefer the strongest realistic isolated environment available (temp app instance, disposable workspace, seeded sandbox, or equivalent) and record the exact command used.

## Review budget
- Low risk: 1 review/fix pass.
- Medium risk: 2 review/fix passes.
- High risk: 3-5 review/fix passes.

## Fast path
- Use for docs-only or low-blast-radius changes.
- Iterate freely, run one required validation pass at the pre-PR gate, then create one focused commit.
- Re-run validation only if the diff changes after review.

## Typical docs validation
```bash
git diff --check
make wiki-sync-check
make preflight
```

## Typical Python validation
```bash
uv run ruff check .
uv run pytest -q
```
