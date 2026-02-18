# Agent Instructions

Use **br** for task tracking and **Agent Mail** for coordination. Keep work scoped to one issue at a time.

## Agent behavior
- Operate as expert full-stack engineers; apply best practices for the language and domain.
- Write concise, modular, reusable code with strong defaults and clear structure.
- Use domain expertise to maximize the product outcome (e.g., UX, performance, reliability).
- Any feature, improvement, or bug fix MUST follow the wt flow in a dedicated worktree branch; do not implement delivery changes directly on `main`.
- Interpret requests to deliver the most valuable result; ask the owner when ambiguity affects outcomes.
- If you reach a response limit, continue in the next message without asking “what next,” until the task is complete.
- Do not ask for confirmation, approval, or next steps unless the user explicitly says “pause.”
- If the user provides a task list or asks you to keep iterating, continue without prompting until blocked or explicitly asked to stop.
- Print `<CONTINUE-LOOP>` as the final line only when at least one task is still pending after the current cycle.

- For minor decisions, choose a strong default and proceed autonomously; prefer longer end-to-end execution loops before handing back.
- Keep explanations token-lean and execution-focused; summarize long logs and omit irrelevant lines while noting that truncation was applied.
- Use the most efficient non-interactive path first (specialized tools for file ops, CLI for git/build/test) to keep runs fast.
- If a mistake happens, report it in chat with a short mistake log (what happened, impact, fix, prevention).
- For easy, low-risk tasks, prioritize fast iteration and avoid heavyweight validation or extra subagent passes.

- When rebasing or syncing with latest `main`, preserve user-authored local changes in touched files while integrating upstream updates.
- Keep implementations lean and semantically structured; add comments/docstrings only when they materially improve clarity.

## Orchestration quickplay
- Default mode: use a short WT flow (implement -> review/fix/improve -> open PR -> merge), then delete the local worktree branch and sync local `main`.
- Open a PR for delivery changes and merge to `main` only through the PR for control and auditability.
- Start in `build` for small, clear, single-scope changes.
- Switch to `orchestrator` when scope spans multiple files/modules, requires sequencing, or needs strict completion gates.
- Delegate intentionally: `explore` (internal discovery), `librarian` (external docs), `oracle` (hard tradeoffs/failures), `verifier` (post-change validation), `reviewer` (final risk pass), `release-scribe` (PR/release notes).
- Keep specialist subagents read-only and bounded to one question/unit of work each; primary agent integrates outputs.
- Do not claim done until implementation, validations, and required review pass (or blocker contract is documented with evidence).
- Under pressure, reduce concurrency first: finish active WT card before opening new long-running continuations.

## 1) Start (every session)
1) Read `AGENTS.md`.
2) If `br` is not initialized, run `br init` once.
3) Run `br ready`, pick one issue, and check the `br-<id>` Mail thread before starting or reviewing.
4) `br update <id> --status in_progress` when you start.
5) Use the br issue id everywhere:
   - Mail `thread_id`: `br-<id>`
   - Subject prefix: `[br-<id>]`
   - File reservation reason: `br-<id>`
   - Optional: include `br-<id>` in commit messages
6) Recommended: set `AGENT_NAME` and use the repo root path as the Mail `project_key`.

`br` never runs git. Keep `.beads/` local, ensure `.gitignore` includes `.beads/`, and do not commit it.
`br` data lives in the current worktree. Create epics/tasks/subtasks in the worktree you are using so each branch keeps its own `.beads/` context, and include epic/task/subtask ids in updates.

## Quick commands
```bash
br ready
br show <id>
br update <id> --status in_progress
br close <id>
br sync --flush-only
```

## 2) Worktrees for new epics/tasks
### wt flow
This flow is required for any feature, improvement, or bug fix:
1) Create a dedicated worktree and branch.
2) Implement in that worktree with small incremental commits.
3) Commit small, focused advances as each logical slice lands (avoid one large batch commit).
4) Run risk-based review/fix/improve passes before opening a PR.
   - Low risk (docs/tests/small scoped edit): 1 pass.
   - Medium risk (typical feature/refactor): 2 passes.
   - High risk (runtime/security/migration): 3-5 passes.
   - Passes may be self-review + verifier/reviewer; do not default every pass to reviewer subagents.
5) Open PR, address review feedback, and re-run checks.
6) Merge when approved; if you are the repository owner, self-merge once checks pass (no extra approval required).
7) Delete the local worktree and branch.
8) Return to `main` and `git pull --rebase`.
9) Stop review cycling once required checks are green and latest review has no blocker findings.

WT execution checklist (use in every run):
- Preflight: `git checkout main && git pull --rebase`, then `git worktree add ../<branch> -b <branch>`; never implement delivery work directly on `main`.
- Tracking: run `br init` (if needed), `br ready`, `br update <id> --status in_progress`, and keep `br-<id>` in updates/threads.
- Delivery: implement in small commits, commit each logical advance, run required checks, open PR, and iterate review/fix/improve until ready to merge.
- Closure: merge PR, delete local worktree + branch, return to `main`, `git pull --rebase`, then close the `br` issue.

WT e2e command flow (reference):
```bash
git checkout main
git pull --rebase
git worktree add ../<branch> -b <branch>
# implement + small commits
git push -u origin <branch>
gh pr create
# after PR merge
git worktree remove ../<branch>
git pull --rebase
```

### Parallel execution (AI runs)
Use one AI run per epic/task, each with its own worktree+branch and `br` issue (`br-<id>`). Prefer OpenCode; Codex/Claude Code are allowed if they follow the same rules.

Task packet (required): epic id, task/subtask ids, scope, acceptance criteria, required checks, constraints, and done definition.

Worker run lifecycle:
1) Implement in its worktree with small incremental commits.
2) Validate required checks/criteria.
3) Open PR, post PR URL in `br-<id>`, then stop.

Coordinator loop (between tasks, only when `ox` is running):
1) Check open PRs; start review/fix runs until criteria pass.
2) Merge PRs with required approvals/checks.
3) Delete merged worktree/branch.
4) Sync `main` (`git pull --rebase`) and rebase active worktrees.

If `ox` is not running, the active agent is the coordinator: run the same loop end-to-end before stopping.

Use subagents only for clean independent splits; never overlap files without explicit reservations.
Limit concurrent subagents to 2 and avoid duplicate role passes on unchanged diffs.

### Build-mode efficiency (default)
When running the `build` agent for normal delivery work:
- Prefer direct implementation and verification before spawning reviewer subagents.
- Reviewer budget by risk:
  - Low risk: 0 reviewer passes (self-check + verifier is enough).
  - Medium risk: max 1 reviewer pass (final gate).
  - High risk: max 2 reviewer passes unless diff materially changed after the latest pass.
- Never run repeated reviewer passes on unchanged diffs.
- For PR merge operations, use `gh pr checks` + `gh pr view --json ...` first; only trigger reviewer if checks fail or code changed.
- Parallelize independent discovery/diagnostics/verification, but keep at most one reviewer and one verifier active at the same time.

### Memory-aware orchestration (default)
Use these rules to avoid session/process pressure regressions during long delivery loops:
- Check pressure before spawning extra passes: if `continue_process_count >= 3`, do not add new reviewer/verifier runs unless a blocker requires it.
- Keep reviewer usage minimal under pressure: one reviewer pass per changed diff; no repeat reviewer pass when code is unchanged.
- Prefer finishing active WT cards over opening new concurrent continuation sessions; avoid stacking parallel long-running sessions on the same repo.
- Time-box long sessions: every 90-120 minutes, checkpoint progress (tests/PR status), then compact or start a fresh session with a short handoff summary.
- When context usage reaches ~55%, run `/compression` and continue with a compact handoff to keep execution stable.
- Escalate only when needed: reserve additional subagents for blocker triage, failing checks, or materially changed diffs.

Pressure mode matrix (deterministic defaults):
- `low` (`continue_process_count < 3`): normal flow; at most one reviewer and one verifier concurrently.
- `medium` (`continue_process_count` in `3..4`): keep one active subagent total; skip non-essential reviewer/verifier passes unless checks fail.
- `high` (`continue_process_count >= 5`): no new reviewer/verifier subagents unless a blocker/severity issue exists; finish in-flight WT task before opening another continuation session.

```bash
# Preferred (OpenCode)
opencode run --agent build --dir ../<branch> "<task-packet>"

# Also valid (Codex / Claude Code)
codex "<task-packet>"
claude "<task-packet>"
```

When starting a new epic or task, create a worktree one folder up.
Name the worktree/branch with a repo prefix for easy identification (e.g., `asx-add-new-ux`).
Run `br` in the worktree you are using (the repo root that contains that branch's `.beads/`).
If unclear, ask the owner. Example: repo `asx`, worktree `../asx-add-new-ux`, `br` runs in `../asx-add-new-ux`.

1) Update main first:
```bash
git checkout main
git pull --rebase
```
2) Create the worktree and branch (same name):
```bash
git worktree add ../<branch> -b <branch>
```
3) Work inside `../<branch>` (do not land delivery edits on `main`).
4) When finished, remove the worktree:
```bash
git worktree remove ../<branch>
```

## 3) Agent Mail coordination
- Register an agent for this repo `project_key` (once per repo): `ensure_project`, then `register_agent`.
- Reserve files before editing: `file_reservation_paths(project_key, agent_name, ["path/**"], ttl_seconds=3600, exclusive=true, reason="br-<id>")`.
- Post updates in the `br-<id>` thread: `send_message(..., thread_id="br-<id>", subject="[br-<id>] Start: <title>")`.
- Check/ack messages: `fetch_inbox`, `acknowledge_message`.
- Release when done: `release_file_reservations(project_key, agent_name, paths=["path/**"])`.
- Multi-agent flow: one agent may create epics/tasks/subtasks, others execute, and another reviews. Always check `br` status and the Mail thread before you start or review.
- Sub-agents: use only for clean splits; each sub-agent registers/reserves and reports in the same `br-<id>` thread. Primary agent integrates/lands changes.

## 4) Python tooling
- Use `uv` for environments and deps.
- Use `ruff` for formatting and fixes: `ruff format`, `ruff check --fix`.

## 5) Project conventions (when missing)
- Create a near-real-time log file per run, overwritten each execution, named `<repo>-<type>.log` (e.g., `asx-web.log`).
- Prefer Makefiles for scripts; provide `make help` with project name/version and concise command descriptions.
- For quick helper scripts (data seeding, checks, one-off migrations), prefer Rust first, then Go, then Python based on fit and speed.
- For web apps, install and use Playwright to simulate the browser and debug UX visually.
- Use pre-commit hooks for lint/format before tests; fix failures, then run tests.
- If pre-commit is missing, install it with `uv` (Python) or the repo's package manager (e.g., npm/pnpm/bun for TS).
- If hook config is missing, add baseline commit hooks that run formatter, linter, and relevant test command(s), then install hooks before committing.
- If commit hooks are not installed locally, install them (`pre-commit install`) and run them once across files (`pre-commit run --all-files`) before the first commit in a task.
- For YAML config examples, include concise comments and explicit option choices when multiple safe defaults exist.
- Add security/static checks to pre-commit when possible:
  - Python/TS: CodeQL + Semgrep (or Semgrep alone for custom rules).
  - Rust: `clippy` + `cargo audit` (Semgrep optional).

## Documentation conventions
- Keep delivery documentation under `docs/`.
- Write planning and rollout docs under `docs/plan/`.
- Write feature/API/behavior specs under `docs/specs/`.
- Prefer short docs that are updated in the same change as code, with clear headings and scoped acceptance criteria.

## 6) Finish (per task)
1) Update docs and tests to match the change.
2) Run required tests/linters/builds and fix failures.
3) Commit changes on your branch.
4) Push the branch and open a PR with clear summary + testing/docs notes.
5) For meaningful changes in git projects, keep commit and push as separate steps.
6) Review the PR before starting new cards; if incomplete, iterate until done.
7) When lint/tests and review pass, merge the PR to `main`.
8) Delete the local worktree and merged branch, then `git pull --rebase` on local `main`.
9) During rebase/merge conflict resolution, preserve user-authored updates in touched files.
10) After completing an epic, create a version tag and release notes with an executive summary and a clear changelog (Adds, Changes, Removals, Fixes).
11) Update `br` status to done/closed when appropriate.
