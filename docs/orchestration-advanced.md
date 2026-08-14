# Orchestration Advanced

Use this guide when work is multi-module, high-risk, dependency-heavy, or running under process pressure.

Primary operating contract is in `AGENTS.md` (adaptive default loop + `wt flow` extension); use this page only when advanced controls are needed. For base GitHub CLI and validation defaults, see `docs/github-cli.md` and `docs/validation-policy.md`.

## Task packets
- Use one AI run per implementation/delivery task. Read-only discovery may inspect local state without a branch, task, session, or remote mutation.
- Every packet names the lane, objective, owned paths/worktree, allowed mutations, prohibited delivery actions, acceptance criteria, checks, stop conditions, and output format.
- Default workers to read-only. Read-only workers cannot edit, commit, push, merge, delete branches/worktrees, or mutate Codememory/GitHub state. A packet that grants mutation must explicitly reclassify the worker as Implementation or Delivery and apply that lane's boundaries.
- Workers return changed paths, command/check results, failures, assumptions, risks, and a done/not-done decision.

## Worker and coordinator flow
- Read-only worker: inspect the assigned scope and return evidence.
- Implementation worker: use the assigned worktree, run the validation policy, and stop after a focused local commit; do not open a PR.
- Delivery worker: only with the Delivery/e2e entry signal; reconcile tracking, run PR checks, open/update the PR, and stop before merge unless the flow authorizes it.
- The coordinator advances automatically when acceptance and checks pass, but never crosses into Delivery without its entry signal.
- For Delivery/e2e only: check PR status/checks and overlaps, recheck `origin/main`, merge only with repository/platform protections satisfied, then clean up and sync.
- Follow `docs/codememory-workflow.md` for tracking/recovery and `docs/validation-policy.md` for checks/review budgets.

## Efficient orchestration
- Implement directly before delegating; delegate only independent discovery, hard tradeoffs, validation, or final-risk review.
- Keep at most one reviewer and one verifier active; do not repeat a pass on an unchanged diff.
- When pressure rises, finish the active slice, checkpoint a compact handoff, and avoid opening continuation/review work unless a blocker requires it.

## Sequencing
- Use Codememory-backed sequencing when dependencies, parallel branches, or handoffs would otherwise be lost.
- Keep the graph compact: objective, child slices, dependencies, checks, and next slice. Skip formal DAGs for tiny work.

## Optional runner commands
```bash
# Preferred (OpenCode)
opencode run --agent build --dir ../<branch> "<task-packet>"

# Also valid (Codex / Claude Code)
codex "<task-packet>"
claude "<task-packet>"
```
