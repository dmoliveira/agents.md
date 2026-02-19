# Orchestration Advanced

Use this guide when work is multi-module, high-risk, or running under process pressure.

## Parallel execution (AI runs)
- Use one AI run per epic/task, each with its own worktree branch and `br` issue (`br-<id>`).
- Use a task packet with: epic/task ids, scope, acceptance criteria, required checks, constraints, and done definition.

Worker lifecycle:
1) Implement in its worktree with small incremental commits.
2) Validate required checks/criteria.
3) Open PR, post PR URL in `br-<id>`, then stop.

Coordinator loop (when `ox` is running):
1) Check open PRs and run review/fix until criteria pass.
2) Merge PRs with required approvals/checks.
3) Delete merged worktree/branch.
4) Sync `main` (`git pull --rebase`) and rebase active worktrees.

If `ox` is not running, the active agent is the coordinator and should run this loop end-to-end.

## Build-mode efficiency
- Prefer direct implementation and verification before reviewer subagents.
- Reviewer budget by risk:
  - Low risk: 0 reviewer passes.
  - Medium risk: max 1 reviewer pass.
  - High risk: max 2 reviewer passes unless diff changed materially.
- Do not repeat reviewer passes on unchanged diffs.
- For PR merge operations, run `gh pr checks` + `gh pr view --json ...` first; use reviewer only when checks fail or code changes.
- Keep concurrency to at most one reviewer and one verifier at a time.

## Validation matrix
- Docs-only (`md`, comments, wording): run `git diff --check`; skip heavy checks unless behavior changed.
- Low-risk code (small, scoped): run targeted lint/test for touched area + one smoke path.
- High-risk/runtime/security/migration: run full required lint/test/build suite and include reviewer/verifier pass.
- Never repeat heavyweight checks on unchanged diffs.

## Memory-aware orchestration
- If `continue_process_count >= 3`, avoid new reviewer/verifier runs unless a blocker requires it.
- Keep reviewer usage minimal under pressure: one reviewer pass per changed diff.
- Prefer finishing active WT cards over opening new long-running continuation sessions.
- Time-box long sessions (90-120 minutes), checkpoint, then compact or restart with a short handoff.
- When context usage reaches about 55%, run `/compression` and continue with a compact handoff.

Pressure mode defaults:
- `low` (`continue_process_count < 3`): normal flow; up to one reviewer and one verifier concurrently.
- `medium` (`continue_process_count` in `3..4`): one active subagent total; skip non-essential reviewer/verifier passes unless checks fail.
- `high` (`continue_process_count >= 5`): no new reviewer/verifier runs unless blocker/severity issue exists.

## Optional runner commands
```bash
# Preferred (OpenCode)
opencode run --agent build --dir ../<branch> "<task-packet>"

# Also valid (Codex / Claude Code)
codex "<task-packet>"
claude "<task-packet>"
```
