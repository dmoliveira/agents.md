# Agent Instructions

Use **br** for task tracking and **Agent Mail** for coordination. Keep work scoped to one issue at a time.

## 1) Start (every session)
1) Read `AGENTS.md`.
2) Run `br ready` and pick one issue (or confirm the human-assigned one).
3) `br update <id> --status in_progress` when you start.
4) Use the br issue id everywhere:
   - Mail `thread_id`: `br-<id>`
   - Subject prefix: `[br-<id>]`
   - File reservation reason: `br-<id>`
   - Optional: include `br-<id>` in commit messages
5) Recommended: set `AGENT_NAME` and use the repo root path as the Mail `project_key`.

`br` never runs git. After `br sync --flush-only`, commit `.beads/` changes.

## 2) Worktrees for new epics/tasks
When starting a new epic or task, create a worktree one folder up.

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

## 3) Agent Mail coordination
- Register an agent for this repo `project_key`.
- Reserve files before editing with the smallest glob (exclusive).
- Post start/progress/done updates in the `br-<id>` thread.
- Release reservations when done.

## 4) Python tooling
- Use `uv` for environments and deps.
- Use `ruff` for formatting and fixes: `ruff format`, `ruff check --fix`.

## 5) Finish (per task)
1) Update docs and tests to match the change.
2) Run required tests/linters/builds and fix failures.
3) Commit changes on your branch.
4) Push the branch and open a PR with clear summary + testing/docs notes.
5) Do not merge; another agent merges the PR.
6) Update `br` status to done/closed when appropriate.
