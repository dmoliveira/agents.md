# Agent Instructions

Use **br** for task tracking and **Agent Mail** for coordination. Keep work scoped to one issue at a time.

## 1) Start (every session)
1) Read `AGENTS.md`.
2) If `br` is not initialized, run `br init` once.
3) Run `br ready` and pick one issue (or confirm the human-assigned one).
4) `br update <id> --status in_progress` when you start.
4) Use the br issue id everywhere:
   - Mail `thread_id`: `br-<id>`
   - Subject prefix: `[br-<id>]`
   - File reservation reason: `br-<id>`
   - Optional: include `br-<id>` in commit messages
6) Recommended: set `AGENT_NAME` and use the repo root path as the Mail `project_key`.

`br` never runs git. After `br sync --flush-only`, commit `.beads/` changes.
`br` data lives in the main project folder. Create epics/tasks/subtasks there so all agents share the same `.beads/` and always include the epic/task/subtask ids in updates.

## 2) Worktrees for new epics/tasks
When starting a new epic or task, create a worktree one folder up.
Keep `br` tracking in the main project folder (the repo root that contains `.beads/`).
If unclear, ask the owner. Example: repo `asx`, worktree `../asx-add-new-ux`, `br` stays in `../asx`.

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

## 4) Python tooling
- Use `uv` for environments and deps.
- Use `ruff` for formatting and fixes: `ruff format`, `ruff check --fix`.

## 5) Finish (per task)
1) Update docs and tests to match the change.
2) Run required tests/linters/builds and fix failures.
3) Commit changes on your branch.
4) Push the branch and open a PR with clear summary + testing/docs notes.
5) Review the PR before starting new cards; if incomplete, iterate until done.
6) When lint/tests and review pass, you may merge to main.
7) Always rebase before merging; coordinate so only one agent merges at a time.
8) During rebase, resolve conflicts carefully so no updates are lost; if unsure, ask the user.
9) After merge, create a version tag and release notes with an executive summary and a clear changelog (Adds, Changes, Removals, Fixes).
10) Update `br` status to done/closed when appropriate.
