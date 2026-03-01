# Operations Loop Runbook

Use this runbook for long-running agent cycles where changes are shipped continuously in small, auditable steps.

## Loop sequence

1. Start from `main`, sync, then create a dedicated worktree branch.
2. Pick one `br` issue and move it to `in_progress`.
3. Implement one scoped slice and commit small.
4. Run lightweight validations relevant to the diff.
5. Open PR, watch checks, merge, and clean up worktree.
6. Sync local `main`, close `br` issue, and continue to next slice.

## Fast preflight

Before each cycle, run:

```bash
make preflight
```

This validates authentication, workflow availability, wiki readiness, and fallback wiki mirror presence.

## If wiki git remote is blocked

If `wiki-status` reports "not ready":

- Keep content updated in `docs/wiki-home-mirror.md`.
- Follow `docs/wiki-bootstrap-runbook.md` for one-time manual provisioning.
- After provisioning, sync mirror content into GitHub Wiki Home page.

## Continuation discipline

- Use short progress messages per cycle.
- Keep each change minimal and reversible.
- Use `<CONTINUE-LOOP>` only when requested work still remains.
