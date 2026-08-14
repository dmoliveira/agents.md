# Validation Policy

Use validation at key gates without adding routine approval pauses. Authority and autonomy rules live in `AGENTS.md`; this page owns checks, risk, review budget, and exit criteria.

## Gate policy
- Validation definition gate (required for non-trivial work): record the checks that prove the slice is done.
- Start gate (required): fetch/check the remote before implementation so the task still matches the latest branch and PR state.
- For iterative or stateful products, when the repo iterative-testing mode is `auto` or `on`, follow `docs/iterative-testing-workflow.md` and prefer validating against the current running state when feasible instead of inferring behavior from files alone.
- During implementation: run quick smoke checks only when needed to unblock risky debugging.
- Pre-PR gate (required): run the selected validation set once on the full current diff.
- When the repo iterative-testing mode is `auto` or `on`, add one best-available sandbox run for important or behavior-heavy changes that exercises the real flow in isolation before claiming confidence.
- Pre-merge gate (conditional): re-run only when code changed after review or CI reported failures.
- Final remote check (required): compare with latest `main` and overlapping PRs right before merge; update if upstream changes would stale or conflict with the current branch.
- When the repo iterative-testing mode is `auto` or `on`, and current live terminal state is needed to validate or debug behavior, use `tmux` if available to inspect live output, keep the process attached, and send non-interactive commands into the running session.
- Fix and rerun failed checks inside the assigned scope and budget. Stop only for credentials, scope expansion, security/privacy, repository/platform protection, or an unresolved blocker; report the boundary.
- For changes to `AGENTS.md`, workflow docs, or skills, add a semantic consistency check across all touched policy files: lane names, authority precedence, Codememory outage behavior, delegation ownership, validation gates, and concise-mode fallback must agree.

Keep validation definitions compact: name only checks that materially prove the slice—docs, lint/tests, UX smoke, real flow, sandbox/live-state run, or a focused harness. Passing evidence advances the authorized slice.

## Read-only and no-change gates

- Read-only/no-diff work needs no implementation test command. Report the searched paths or queries, the evidence gathered, and the resulting decision.
- If an implementation produces no diff, verify that the requested outcome already exists and cite the evidence. Otherwise treat no-change as unmet acceptance, not as a successful empty commit or PR.

## Risk matrix
- Docs-only: run `git diff --check`; skip heavier checks unless behavior changed.
- Low-risk code: run targeted lint/test for the touched area plus one smoke path.
- Iterative/stateful flows: when the repo iterative-testing mode is `auto` or `on`, add a live smoke path against the running process or session state when that is where failures surface.
- High-risk/runtime/security/migration: run full required lint/test/build suite.
- Important runtime changes: when the repo iterative-testing mode is `auto` or `on`, prefer the strongest realistic isolated environment available (temp app instance, disposable workspace, seeded sandbox, or equivalent) and record the exact command used.

## Review budget
- Low risk: 1 review/fix pass.
- Medium risk: 2 review/fix passes, performed as AI evidence loops unless repository/platform rules require an external approver.
- High risk: 3-5 review/fix passes.
- A repeat pass needs changed evidence, a failed check, or newly discovered risk; do not duplicate the same verifier/reviewer pass on an unchanged diff.
- The count is a ceiling, not a reason to add passes; stop when checks are green and the latest changed-diff review has no blocker.

## Fast path
- Use for docs-only or low-blast-radius changes.
- Keep the validation definition to one short statement, run one required validation pass at the pre-PR gate, then create one focused commit.
- Re-run validation only if the diff changes after review.

## Optional module toggle
- Treat iterative/live-state testing as an optional repo module with modes `off`, `auto`, and `on`. See `AGENTS.md` for precedence and `docs/iterative-testing-workflow.md` for operational detail.

## Default local docs validation
```bash
git diff --check
```

## Conditional repository readiness

Run these only when the slice affects the wiki mirror or remote delivery:

```bash
make wiki-sync-check  # mirror-controlled docs
make preflight        # authenticated GitHub/workflow/wiki readiness
```

## Typical Python validation
```bash
python3 -m py_compile <touched-files>
uv run ruff check .
uv run pytest -q
```
