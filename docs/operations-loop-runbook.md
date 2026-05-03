# Operations Loop Runbook

Use this runbook for long-running agent cycles where changes are shipped continuously in small, auditable steps.

For the full docs map, start with `docs/index.md`.

## Loop sequence

This runbook extends the canonical adaptive loop from `AGENTS.md` for long-running delivery work.

1. Resume/alignment: start from `main`, sync, fetch/check remote branch and PR state, and check Codememory with `oc current`, `oc next`, `oc queue`, or `oc resume --task <id>`.
2. Open or resume one dedicated worktree branch and bind the active Codememory task/session to it.
3. Classify the slice (`small` / `medium` / `large`) and do only the research needed for safe progress.
4. Record the active plan slice plus validation definition before coding. Add dependencies/sequence when the work is `medium` or `large`.
5. Implement one scoped slice with fast local iteration and continue while the next safe action is clear.
6. Run the required validation gate, update Codememory with the latest validated outcome, and create one focused commit for the validated slice.
7. If delivery is in scope, open/update the PR, watch checks, do one final overlap check against latest `main`, merge, and clean up the worktree.
8. Sync local `main`, close/update the issue or task, then continue to the next slice.

## Fast preflight

Before each cycle, run:

```bash
make preflight
```

This validates authentication, workflow availability, wiki readiness, and fallback wiki mirror presence.

It also runs wiki consistency checks to ensure snippet and mirror content stay aligned.

For the full Codememory startup and closeout flow, see `docs/codememory-workflow.md`. For validation-definition and gate policy, see `docs/validation-policy.md`.

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
- Use `<CONTINUE-LOOP>` when work still remains or the next plan slice is already clear.
