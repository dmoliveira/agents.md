# Validation Policy

Use validation at key gates so iteration stays fast without skipping quality checks.

## Gate policy
- Validation definition gate (required for non-trivial work): before implementation, name the checks that will prove the slice is done.
- Start gate (required): fetch/check the remote before implementation so the task still matches the latest branch and PR state.
- For iterative or stateful products, when the repo iterative-testing mode is `auto` or `on`, follow `docs/iterative-testing-workflow.md` and prefer validating against the current running state when feasible instead of inferring behavior from files alone.
- During implementation: run quick smoke checks only when needed to unblock risky debugging.
- Pre-PR gate (required): run the selected validation set once on the full current diff.
- When the repo iterative-testing mode is `auto` or `on`, add one best-available sandbox run for important or behavior-heavy changes that exercises the real flow in isolation before claiming confidence.
- Pre-merge gate (conditional): re-run only when code changed after review or CI reported failures.
- Final remote check (required): compare with latest `main` and overlapping PRs right before merge; update if upstream changes would stale or conflict with the current branch.
- When the repo iterative-testing mode is `auto` or `on`, and current live terminal state is needed to validate or debug behavior, use `tmux` if available to inspect live output, keep the process attached, and send non-interactive commands into the running session.

Validation definition should be compact but explicit. Name only the checks that matter for the slice: docs validation, lint/unit/integration tests, UX smoke path, frontend/backend behavior, sandbox/live-state run, or debug harness/scripts when they materially improve confidence.

## Risk matrix
- Docs-only: run `git diff --check`; skip heavier checks unless behavior changed.
- Low-risk code: run targeted lint/test for the touched area plus one smoke path.
- Iterative/stateful flows: when the repo iterative-testing mode is `auto` or `on`, add a live smoke path against the running process or session state when that is where failures surface.
- High-risk/runtime/security/migration: run full required lint/test/build suite.
- Important runtime changes: when the repo iterative-testing mode is `auto` or `on`, prefer the strongest realistic isolated environment available (temp app instance, disposable workspace, seeded sandbox, or equivalent) and record the exact command used.

## Review budget
- Low risk: 1 review/fix pass.
- Medium risk: 2 review/fix passes.
- High risk: 3-5 review/fix passes.

## Fast path
- Use for docs-only or low-blast-radius changes.
- Keep the validation definition to one short statement, run one required validation pass at the pre-PR gate, then create one focused commit.
- Re-run validation only if the diff changes after review.

## Optional module toggle
- Treat iterative/live-state testing as an optional repo module with modes `off`, `auto`, and `on`. See `AGENTS.md` for precedence and `docs/iterative-testing-workflow.md` for operational detail.

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
