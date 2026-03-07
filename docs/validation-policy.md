# Validation Policy

Use validation at key gates so iteration stays fast without skipping quality checks.

## Gate policy
- Pre-PR gate (required): run the selected validation set once on the full current diff.
- Pre-merge gate (conditional): re-run only when code changed after review or CI reported failures.
- During implementation: run quick smoke checks only when needed to unblock risky debugging.

## Risk matrix
- Docs-only: run `git diff --check`; skip heavier checks unless behavior changed.
- Low-risk code: run targeted lint/test for the touched area plus one smoke path.
- High-risk/runtime/security/migration: run full required lint/test/build suite.

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
