# Operations Loop Runbook

Use this runbook for long-running agent cycles where changes are shipped continuously in small, auditable steps.

## Loop sequence

1. Start from `main`, sync, then create a dedicated worktree branch.
2. Pick one GitHub issue and move it to `in_progress` using labels/status/projects.
3. Implement one scoped slice and commit small.
4. Run lightweight validations relevant to the diff.
5. Open PR, watch checks, merge, and clean up worktree.
6. Sync local `main`, close the issue, and continue to next slice.

## Fast preflight

Before each cycle, run:

```bash
make preflight
```

This validates authentication, workflow availability, wiki readiness, and fallback wiki mirror presence.

It also runs wiki consistency checks to ensure snippet and mirror content stay aligned.

## If wiki git remote is blocked

If `wiki-status` reports "not ready":

- Keep content updated in `docs/wiki-home-mirror.md`.
- Follow `docs/wiki-bootstrap-runbook.md` for one-time manual provisioning.
- Use `docs/wiki-publish-alternatives.md` for approved fallback publication paths.
- After provisioning, sync mirror content into GitHub Wiki Home page.

After provisioning, run:

```bash
make wiki-sync-dry-run
make wiki-sync-apply
```

If provisioning continues to fail but publication is required, run:

```bash
make wiki-fallback-sync-dry-run
make wiki-fallback-sync-apply
```

For CI automation, set repository secret `FALLBACK_REPO_TOKEN` and trigger:

```bash
make wiki-fallback-dispatch
```

To monitor readiness between cycles, trigger:

```bash
make wiki-probe-dispatch
```

## Continuation discipline

- Use short progress messages per cycle.
- Keep each change minimal and reversible.
- Use `<CONTINUE-LOOP>` only when requested work still remains.
