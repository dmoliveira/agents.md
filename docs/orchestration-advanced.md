# Orchestration Advanced

Use this guide when work is multi-module, high-risk, dependency-heavy, or running under process pressure.

Primary operating contract is in `AGENTS.md` (adaptive default loop + `wt flow` extension); use this page only when advanced controls are needed. For base GitHub CLI and validation defaults, see `docs/github-cli.md` and `docs/validation-policy.md`.

## Parallel execution (AI runs)
- Use one AI run per epic/task, each with its own worktree branch, Codememory task/session context, and a tracked GitHub issue when delivery tracking is needed.
- Use a task packet with: epic/task ids, scope, acceptance criteria, required checks, constraints, and done definition.

Worker lifecycle:
1) Check remote branch/PR state before implementation so the assigned slice still matches upstream and overlapping AI work.
2) Recover or create Codememory task/session state for the assigned slice.
3) Classify execution depth/risk, do targeted research, and capture the plan + validation definition before coding.
4) If sequencing matters, preserve dependencies/parallelism in Codememory so the execution graph survives handoff or resume.
5) Implement in its worktree with fast local iteration.
6) Run required checks at the pre-PR gate, update Codememory outcome state, and create one focused commit for the validated slice.
7) Open PR, post PR URL on the related issue, then stop.

Coordinator loop (when `ox` is running):
1) Check open PRs and run review/fix until criteria pass.
2) Re-check `main` and overlapping PRs/branches right before merge so late upstream changes do not stale out active work.
3) Merge PRs with required approvals/checks.
4) Delete merged worktree/branch.
5) Sync `main` (`git pull --rebase`) and rebase active worktrees.

If `ox` is not running, the active agent is the coordinator and should run this loop end-to-end.

## Build-mode efficiency
- Prefer direct implementation and verification before reviewer subagents.
- If repeated shell retries are only blocked by UI-owned state, switch to the browser workflow in `docs/agent-browser.md` instead of adding more shell churn.
- Reviewer/verifier usage should defer to the canonical review budget in `AGENTS.md` and `docs/validation-policy.md`.
- Prefer the lightest reviewer usage that still satisfies that budget.
- Do not repeat reviewer passes on unchanged diffs.
- For PR merge operations, run `gh pr checks` + `gh pr view --json ...` first; use reviewer only when checks fail or code changes.
- Keep concurrency to at most one reviewer and one verifier at a time.

## Sequencing and DAG guidance
- Use Codememory-backed sequencing only when dependencies, parallel branches of work, or likely handoffs would otherwise get lost.
- Prefer a compact execution graph: objective, child slices, dependency edges, required checks, and current next slice.
- Do not build a formal DAG for tiny work that can be carried safely in one short plan.

## Validation matrix
- Follow `docs/validation-policy.md` for the base gate policy and task-type defaults.
- Add reviewer/verifier passes when scope or risk exceeds the base policy.
- For important or behavior-heavy changes, prefer one sandboxed end-to-end validation pass over multiple weaker speculative checks.

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
