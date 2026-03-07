# Agent Instructions

Use native repo tooling available in this environment (`git`, `gh`, and built-in agent tools). Keep work scoped to one issue/task at a time.

## Quickstart
- Follow `## 1) Start (every session)` and pick one scoped issue/task.
- Use `## 2) Worktrees for new epics/tasks` for all delivery work (never land changes on `main`).
- Use `## 6) Finish (per task)` for commit, PR, merge, cleanup, and sync steps.
- Use `## 7) Final response pattern` for `<CONTINUE-LOOP>` and completion suggestions.
- Use `docs/tooling-quick-ref.md` and `docs/orchestration-advanced.md` for fast commands and advanced controls.

## Directive levels
- `MUST`: mandatory; do not skip unless the user explicitly overrides.
- `SHOULD`: default behavior; deviate only with a clear reason.
- `MAY`: optional optimization.

## Decision order
- When instructions conflict, apply this order: `AGENTS.md` > user task prompt > general defaults.
- `Pending tasks` means any requested scope item not fully completed and validated yet.

## Quick glossary
- `Pending tasks`: requested scope items not fully completed and validated yet.
- `Pass`: one review/fix/improve cycle over the current diff and checks.
- `Blocker`: a concrete issue preventing safe progress (missing credential, failing dependency, policy gate, or hard error).

## Agent behavior
- Operate as expert full-stack engineers; apply best practices for the language and domain.
- Write concise, modular, reusable code with strong defaults and clear structure.
- Use domain expertise to maximize the product outcome (e.g., UX, performance, reliability).
- Any feature, improvement, or bug fix MUST follow the wt flow in a dedicated worktree branch; do not implement delivery changes directly on `main`.
- Never repurpose `main` as a delivery branch; keep `main` for sync/merge only and do implementation in worktree branches (MUST).
- Interpret requests to deliver the most valuable result; ask the owner when ambiguity affects outcomes.
- If you reach a response limit, continue in the next message without asking “what next,” until the task is complete.
- Do not ask for confirmation, approval, or next steps unless the user explicitly says “pause.”
- If the user provides a task list or asks you to keep iterating, continue without prompting until blocked or explicitly asked to stop.
- Print `<CONTINUE-LOOP>` as the final line only when at least one task is still pending after the current cycle.
- If one task is complete but additional requested tasks remain, continue execution and keep `<CONTINUE-LOOP>` as the final line for that cycle.
- If all requested tasks are complete and no pending items remain, provide concise next-step suggestions proactively.

- For minor decisions, choose a strong default and proceed autonomously; prefer longer end-to-end execution loops before handing back (SHOULD).
- Keep explanations token-lean and execution-focused; summarize long logs and omit irrelevant lines while noting that truncation was applied.
- Use the most efficient non-interactive path first (specialized tools for file ops, CLI for git/build/test) to keep runs fast (SHOULD).
- For independent repeated commands, prefer `parallel` over shell `for` loops; use `xargs -P` or sequential execution only when needed.
- Non-interactive checklist: avoid editors/pagers/REPLs, always pass non-interactive flags (`--yes`, `--no-edit`, `--non-interactive`) when available, and use explicit commit messages.
- If a mistake happens, report it in chat with a short mistake log (what happened, impact, fix, prevention).
- When available, use `my_opencode` mistake/learning tooling to avoid repeated failures (`plugin/gateway-core/docs/mistake-ledger-report.md`, `/learn capture|review|publish|search|doctor`).
- Suggested monthly cadence: review `mistake:report --mode digest --json` trends and convert stable lessons into `/learn` entries.
- For easy, low-risk tasks, prioritize fast iteration and avoid heavyweight validation or extra subagent passes (SHOULD).

- When rebasing or syncing with latest `main`, preserve user-authored local changes in touched files while integrating upstream updates.
- Keep implementations lean and semantically structured; add comments/docstrings only when they materially improve clarity.

## Orchestration quickplay
- Default mode: use a short WT flow (implement -> review/fix/improve -> open PR -> merge), then delete the local worktree branch and sync local `main`.
- Prefer one focused commit per validated feature/task slice instead of many intermediate commits.
- Open a PR for delivery changes and merge to `main` only through the PR for control and auditability (MUST).
- For local productivity shortcuts, use `docs/tooling-quick-ref.md` (primary source: `../my_utils`, fallback: `../utils-scripts`).
- Start in `build` for small, clear, single-scope changes (SHOULD).
- Switch to `orchestrator` when scope spans multiple files/modules, requires sequencing, or needs strict completion gates.
- Delegate intentionally: `explore` (internal discovery), `librarian` (external docs), `oracle` (hard tradeoffs/failures), `verifier` (post-change validation), `reviewer` (final risk pass), `release-scribe` (PR/release notes).
- Keep specialist subagents read-only and bounded to one question/unit of work each; primary agent integrates outputs.
- Do not claim done until implementation, validations, and required review pass (or blocker contract is documented with evidence).
- Under pressure, reduce concurrency first: finish active WT card before opening new long-running continuations.

### Fast path (low risk)
- Use this for docs-only changes or small, scoped edits with low blast radius.
- Iterate quickly without running full lint/tests on every local change.
- Run one required validation pass at the pre-PR gate, then create one focused commit.
- Re-run validation only if code changes after review or CI reports failures.
- Keep review/fix passes lean (typically one pass) unless a blocker appears.

## 1) Start (every session)
1) Read `AGENTS.md`.
2) Review open issues/PRs and pick one scoped item to deliver.
3) Mark the item `in_progress` using native tracker capabilities when available (GitHub labels/status/projects).
4) Use the issue/task id in branch names, commits, and PR titles when practical.
5) Keep all execution in a dedicated worktree branch for that item.

## Quick commands
```bash
gh issue list --state open --limit 20
gh issue view <id>
gh pr status
git status
git worktree list
```

## 2) Worktrees for new epics/tasks
### wt flow
This flow is required for any feature, improvement, or bug fix:
1) Create a dedicated worktree and branch.
2) Implement in that worktree with fast local iteration.
3) Create one focused commit when the slice is complete and validated at the pre-PR gate.
4) Run risk-based review/fix/improve passes at key gates before opening a PR.
   - Pre-PR gate (required): run the required lint/tests/build once for the current diff.
   - Pre-merge gate (conditional): re-run checks only when code changes after review or CI reports failures.
   - Low risk (docs/tests/small scoped edit): 1 pass.
   - Medium risk (typical feature/refactor): 2 passes.
   - High risk (runtime/security/migration): 3-5 passes.
   - Passes may be self-review + verifier/reviewer; do not default every pass to reviewer subagents.
5) Open PR, address review feedback, and re-run checks.
6) Merge when approved; if you are the repository owner, self-merge once checks pass (no extra approval required).
7) Delete the local worktree and branch.
8) Return to `main` and `git pull --rebase`.
9) Stop review cycling once required checks are green and latest review has no blocker findings.

WT execution checklist (canonical):
- Use `wt flow` steps 1-9 above as the single source of truth for implementation, review, PR, merge, and cleanup.
- Keep issue/PR status updated through start, progress, and completion.

WT e2e command flow (reference):
```bash
git checkout main
git pull --rebase
git worktree add ../<branch> -b <branch>
# implement + validate (pre-PR gate)
# create one focused commit
git push -u origin <branch>
gh pr create
# after PR merge
git worktree remove ../<branch>
git pull --rebase
```

### Advanced orchestration
- For multi-agent execution, reviewer/verifier budgets, validation matrix, and memory-pressure playbooks, see `docs/orchestration-advanced.md`.
- Use advanced controls when scope, risk, or process pressure requires them; otherwise follow `Orchestration quickplay` and `wt flow`.

When starting a new epic or task, follow the `wt flow` and `WT e2e command flow` above; keep branch names repo-prefixed (for example, `asx-add-new-ux`).

## 3) Native coordination
- Use GitHub Issues/PRs as the source of truth for task state and handoffs.
- For multi-agent or multi-step work, post concise progress/blocker updates in issue or PR comments.
- Keep ownership explicit by naming the active task id in branch, commit, and PR metadata when practical.
- Share validation evidence (commands and outcomes) in PR descriptions or final task notes.

## 4) Python tooling
- Use `uv` for environments and deps.
- Use `ruff` for formatting and fixes: `ruff format`, `ruff check --fix`.

## 5) Project conventions (when missing)
- Create a near-real-time log file per run, overwritten each execution, named `<repo>-<type>.log` (e.g., `asx-web.log`).
- Prefer Makefiles for scripts; provide `make help` with project name/version and concise command descriptions.
- For quick helper scripts (data seeding, checks, one-off migrations), prefer Rust first, then Go, then Python based on fit and speed.
- For web apps, install and use Playwright to simulate the browser and debug UX visually.
- Prefer running lint/tests at key gates (pre-PR required, pre-merge conditional) rather than on every local iteration.
- If pre-commit is configured, use it as part of the pre-PR gate to catch issues before review.
- If pre-commit is missing, installation is optional; prioritize CI and explicit pre-PR validation commands.
- If hook config is missing, prefer lightweight CI checks over strict local hook setup.
- For YAML config examples, include concise comments and explicit option choices when multiple safe defaults exist.
- Add security/static checks to pre-commit when possible:
  - Python/TS: CodeQL + Semgrep (or Semgrep alone for custom rules).
  - Rust: `clippy` + `cargo audit` (Semgrep optional).

## Documentation conventions
- Keep delivery documentation under `docs/`.
- Write planning and rollout docs under `docs/plan/`.
- Write feature/API/behavior specs under `docs/specs/`.
- Keep tooling quick references under `docs/` (current: `docs/tooling-quick-ref.md`).
- Keep advanced orchestration guidance under `docs/` (current: `docs/orchestration-advanced.md`).
- Prefer short docs that are updated in the same change as code, with clear headings and scoped acceptance criteria.

## 6) Finish (per task)
1) Update docs and tests to match the change.
2) Run required tests/linters/builds at the pre-PR gate and fix failures.
3) Commit the validated changes on your branch (prefer one focused commit per completed slice).
4) Push the branch and open a PR with clear summary + testing/docs notes.
5) For meaningful changes in git projects, keep commit and push as separate steps.
6) Review the PR before starting new cards; if incomplete, iterate until done.
7) When lint/tests and review pass, merge the PR to `main`.
8) Delete the local worktree and merged branch, then `git pull --rebase` on local `main`.
9) During rebase/merge conflict resolution, preserve user-authored updates in touched files.
10) After completing an epic, create a version tag and release notes with an executive summary and a clear changelog (Adds, Changes, Removals, Fixes).
11) Update issue/task status to done/closed when appropriate.
12) If additional requested tasks remain after this cycle, end with `<CONTINUE-LOOP>` on the final line.
13) If no pending tasks remain, end with concise next-step suggestions (do not hand off with only a question).

## 7) Final response pattern
- If work remains: brief progress + blocker/next action + final line `<CONTINUE-LOOP>`.
- If work is complete: brief outcome + validation evidence + 1-3 concise next-step suggestions.

Examples:
- Pending: "Updated API retries and fixed tests; awaiting production API key for live validation. Next: run final smoke once key is provided." + final line `<CONTINUE-LOOP>`.
- Complete: "Added retry/backoff support, validated with `pytest -q` and `ruff check .`, and merged PR #123." Then list 1-3 concise next-step suggestions.
- Complete (docs-only fast path): "Updated docs for WT flow clarity, validated with `git diff --check`, and merged PR #123." Then list 1-2 concise next-step suggestions.

Anti-loop guard examples:
- Continue: one requested item completed, but additional requested items remain -> keep executing and end with `<CONTINUE-LOOP>`.
- Stop: all requested items completed and validated -> provide concise next-step suggestions and do not emit `<CONTINUE-LOOP>`.
- Blocked: include blocker reason, evidence, and next best action; if requested work still remains after the report, end with `<CONTINUE-LOOP>`.

Blocker contract template:
- `BLOCKER:` <exact reason>
- `EVIDENCE:` <file/command/error>
- `NEXT:` <best next action>
