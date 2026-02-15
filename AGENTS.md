# Agent Instructions

Use **br** for task tracking and **Agent Mail** for coordination. Keep work scoped to one issue at a time.

## Agent behavior
- Operate as expert full-stack engineers; apply best practices for the language and domain.
- Write concise, modular, reusable code with strong defaults and clear structure.
- Use domain expertise to maximize the product outcome (e.g., UX, performance, reliability).
- Interpret requests to deliver the most valuable result; ask the owner when ambiguity affects outcomes.
- If you reach a response limit, continue in the next message without asking “what next,” until the task is complete.
- Do not ask for confirmation, approval, or next steps unless the user explicitly says “pause.”
- If the user provides a task list or asks you to keep iterating, continue without prompting until blocked or explicitly asked to stop.

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

`br` never runs git. Keep `.beads/` local (gitignored) and do not commit it.
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
Use this flow for each request/feature/fix:
1) Create a dedicated worktree and branch.
2) Implement in that worktree with small incremental commits.
3) Run at least 5 review/fix/improve passes before opening a PR.
4) Open PR, address review feedback, and re-run checks.
5) Merge when approved.
6) Delete the worktree and branch.
7) Return to `main` and `git pull --rebase`.

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
3) Work inside `../<branch>`.
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
- Prefer Makefiles for scripts; provide `make help` with command names and short descriptions.
- For web apps, install and use Playwright to simulate the browser and debug UX visually.
- Use pre-commit hooks for lint/format before tests; fix failures, then run tests.
- If pre-commit is missing, install it with `uv` (Python) or the repo's package manager (e.g., npm/pnpm/bun for TS).
- If hook config is missing, add baseline commit hooks that run formatter, linter, and relevant test command(s), then install hooks before committing.
- If commit hooks are not installed locally, install them (`pre-commit install`) and run them once across files (`pre-commit run --all-files`) before the first commit in a task.
- Add security/static checks to pre-commit when possible:
  - Python/TS: CodeQL + Semgrep (or Semgrep alone for custom rules).
  - Rust: `clippy` + `cargo audit` (Semgrep optional).

## 6) Finish (per task)
1) Update docs and tests to match the change.
2) Run required tests/linters/builds and fix failures.
3) Commit changes on your branch.
4) Push the branch and open a PR with clear summary + testing/docs notes.
5) For meaningful changes in git projects, keep commit and push as separate steps.
6) Review the PR before starting new cards; if incomplete, iterate until done.
7) When lint/tests and review pass, you may merge to main.
8) Always rebase before merging; coordinate so only one agent merges at a time.
9) During rebase, resolve conflicts carefully so no updates are lost; if unsure, ask the user.
10) After merge, create a version tag and release notes with an executive summary and a clear changelog (Adds, Changes, Removals, Fixes).
11) Update `br` status to done/closed when appropriate.
