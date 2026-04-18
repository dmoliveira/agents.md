# Agent Instructions

Use native repo tooling available in this environment (`git`, `gh`, `oc`, and built-in agent tools). Keep work scoped to one issue/task at a time.

## Quickstart
- Read `AGENTS.md`, pick one scoped issue/task, and execute in a dedicated worktree branch.
- Use `wt flow` for all delivery work; never land feature changes directly on `main`.
- Keep issue/PR status updated through start, progress, and completion.
- Use `docs/tooling-quick-ref.md`, `docs/codememory-workflow.md`, `docs/codememory-conventions.md`, `docs/github-cli.md`, `docs/validation-policy.md`, and `docs/orchestration-advanced.md` as supporting references.
- For optional external operator help, use the curated references listed in `docs/tooling-quick-ref.md` instead of loading broad external repo context.

## Directive levels
- `MUST`: mandatory unless the user explicitly overrides.
- `SHOULD`: default behavior; deviate only with a clear reason.
- `MAY`: optional optimization.

## Decision order
- Follow this precedence: `AGENTS.md` > user request > general defaults.
- `Pending tasks` means requested scope not yet completed and validated.
- `Blocker` means a concrete issue preventing safe progress.

## Core behavior
- Operate as an expert engineer: concise, modular, pragmatic, and outcome-focused.
- Choose strong defaults for minor decisions and keep execution moving until done or blocked.
- Continue executing while there is a clear next action; do not stop merely to restate a plan or wait for routine confirmation.
- On resumed sessions, re-read `AGENTS.md` and any directly relevant workflow docs before continuing so the latest repo instructions override stale session context.
- For user-visible progress notes, command/test reporting, and rationale summaries, prefix each reporting block with a local timestamp collected from the shell at runtime (for example via `date`) so execution traces are easier to follow without adding noise to every line.
- When a command/log/telemetry example includes the runtime session id, include a timestamp variable collected from the shell too (for example `TS="$(date +"%Y-%m-%dT%H:%M:%S%z")"`) so execution time is explicit and not auto-generated from memory.
- Do not ask for confirmation unless ambiguity materially changes the result or a secret/credential is required.
- Do not hand low-impact decisions back to the user when the repo context already makes a reasonable choice clear; pick the strong default and keep moving.
- Treat naming, file placement, ordering, wording, and similarly small implementation details as agent-owned decisions unless the user explicitly asks to control them.
- Prefer making the next reasonable decision, documenting the rationale briefly, and advancing the task as far as safely possible in one run.
- Keep explanations lean; summarize long logs and keep evidence relevant.
- When asked for the current runtime session id, output only the exact id from the session context and nothing else. Do not add acknowledgements, explanations, paraphrases, punctuation, or substitute another value.
- Check the remote state before starting implementation so the chosen task still matches the latest branch and PR state.
- Preserve user-authored changes when syncing or resolving conflicts in touched files.
- Keep implementations semantically structured; add comments only when they materially help.

## Delivery rules
- Any feature, improvement, or bug fix MUST use a dedicated worktree branch.
- Never repurpose `main` as a delivery branch; use `main` only for sync/merge.
- Prefer one focused commit per validated feature/task slice instead of many intermediate commits.
- Open a PR for delivery changes and merge to `main` only through the PR.
- Keep commit and push as separate steps for meaningful changes.
- When a user asks to do work "end-to-end", "e2e", or with equivalent shorthand, treat that as default authorization to run the full `wt flow` for the scoped request: split the work into focused validated slices when needed, commit the validated slice(s), open the PR, run the required risk-based review/fix/improve loop until the latest pass has no blocker findings, merge when checks are clear, delete the merged worktree/branch, and sync local `main`, unless the user explicitly narrows or overrides part of that flow.

## Codememory coordination
- Codememory is REQUIRED in this repo for internal execution tracking, handoffs, durable learnings, and resumable AI coordination.
- Treat Codememory as the source of truth for internal execution state; treat GitHub as the source of truth for delivery state, reviews, and merges.
- Use Codememory instead of ad hoc todo lists for meaningful work.
- Do not use OpenCode's `todowrite`/todo list for task coordination in this repo; use Codememory (`oc`) instead.
- Before starting or resuming meaningful work, check Codememory first with the startup flow in `docs/codememory-workflow.md`.
- Every meaningful request that creates work MUST create or attach to a Codememory `task` or `epic` before implementation continues.
- Every active implementation attempt MUST have a Codememory `session` tied to the active worktree path.
- Record durable blockers, decisions, ideas, assumptions, conventions, and handoff context in Codememory so another AI can resume without relying on chat history.
- Keep Codememory-specific commands and conventions in the dedicated Codememory docs so future updates or temporary disablement stay localized.

## Validation and review
- Default to fast local iteration; avoid heavyweight checks on every edit.
- Run the required validation set at the pre-PR gate for the full current diff.
- Re-run validation at the pre-merge gate only when code changed after review or CI reported failures.
- Before merge, do one last remote sync check on `main` and any overlapping PRs so new upstream changes do not stale out or conflict with the branch being merged.
- Low risk (docs/tests/small scoped edit): 1 review/fix pass.
- Medium risk (typical feature/refactor): 2 review/fix passes.
- High risk (runtime/security/migration): 3-5 review/fix passes.
- Stop review cycling once required checks are green and the latest review has no blocker findings.
- For docs-only or low-blast-radius changes, use the fast path in `docs/validation-policy.md`.

## Orchestration quickplay
- Start in `build` for small, clear, single-scope changes.
- Switch to `orchestrator` when scope spans multiple files/modules, requires sequencing, or needs strict completion gates.
- Delegate intentionally: `explore` for discovery, `librarian` for external docs, `oracle` for hard tradeoffs, `verifier` for validation, `reviewer` for final risk review, `release-scribe` for PR/release text.
- Keep specialist subagents read-only and bounded; the primary agent integrates and lands changes.
- Under pressure, reduce concurrency first and finish the active worktree card before opening another.

## 1) Start (every session)
1) Read `AGENTS.md`.
   - If resuming a previous session, re-read `AGENTS.md` plus any relevant docs you will rely on before taking the next action.
2) Fetch/check the remote so local context matches the latest branch and PR state.
3) Check Codememory startup context with `oc current`, `oc next`, `oc queue`, or `oc resume --task <id>` as appropriate.
4) Review open issues/PRs and pick one scoped item to deliver.
5) Confirm the selected scope still fits the latest upstream branch state and does not duplicate overlapping in-flight work.
6) Create or attach the work to a Codememory `task` or `epic`, then mark the item `in_progress` using native tracker capabilities when available.
7) Use the issue/task id in branch names, commits, and PR titles when practical.
8) Keep all execution in a dedicated worktree branch for that item and bind the active Codememory session to that worktree.

## 2) Worktrees for new epics/tasks
### wt flow
1) Create a dedicated worktree and branch.
2) Fetch/check the remote branch state before implementation so the task starts from current upstream context.
3) Start or resume a Codememory session for that worktree and attach it to the active task.
4) Implement in that worktree with fast local iteration.
5) Record durable execution state in Codememory as the work evolves.
6) Run the pre-PR validation gate for the current diff.
7) Create one focused commit for the validated slice.
8) Push the branch and open a PR.
9) Address review feedback and re-run checks only when needed.
10) Before merge, re-check `origin/main` plus overlapping PRs/branches for late conflicts or duplicated functionality.
11) Close the Codememory task/session state when the slice is done, failed, or canceled.
12) Merge when checks pass.
13) Delete the local worktree and branch.
14) Return to `main` and `git pull --rebase`.

### Fast path
- Use for docs-only changes or small scoped edits with low blast radius.
- Iterate quickly, run one required validation pass at the pre-PR gate, and create one focused commit.

## 3) Native coordination
- Use Codememory as the source of truth for internal task state, AI handoffs, and resumable execution context.
- Use GitHub Issues/PRs as the source of truth for delivery state, review state, and merge state.
- Post concise progress or blocker updates in issue/PR comments when helpful.
- Share validation evidence in PR descriptions or final task notes.

## 4) Project conventions
- Use `uv` for Python environments/dependencies and `ruff` for Python formatting/fixes.
- Prefer Makefiles for repeatable repo scripts; use `make help` first.
- Prefer running lint/tests at key gates instead of on every local iteration.
- If pre-commit is configured, use it at the pre-PR gate; if missing, installation is optional.
- Keep delivery documentation under `docs/`, with long-form planning docs organized by status under `docs/plan/{new,doing,blocked,parked,done,cancelled}` and specs in `docs/specs/`. Codememory remains the primary execution tracker.

## 5) Finish (per task)
1) Update docs and tests to match the change.
2) Run the required pre-PR validations and fix failures.
3) Update Codememory records so the task and session reflect the validated outcome, blockers, and durable learnings.
4) Commit the validated changes on your branch.
5) Push the branch and open a PR with summary and validation notes.
6) Review the PR before starting new work; iterate until complete.
7) Re-check `main` and relevant overlapping PRs right before merge; update/rebase if upstream changed in a way that affects your slice.
8) Merge when checks, review, and the final remote alignment check pass.
9) Delete the local worktree and merged branch, then sync local `main`.
10) Update GitHub issue/task status to done/closed when appropriate.

## 6) Final response pattern
- If work remains or a clear next execution step is already known: brief progress + blocker/next action + final line `<CONTINUE-LOOP>`.
- If work is complete: brief outcome + validation evidence + optional follow-up suggestions only when no further in-scope execution is pending.
- Use `<CONTINUE-LOOP>` whenever the task is not fully done and the next plan slice is already identifiable, even if the remaining work is small.
- Do not frame pending in-scope work as "best next steps" or optional suggestions; treat it as continuation and end with `<CONTINUE-LOOP>`.
- Do not ask the user to break ties between equivalent low-risk options when one reasonable default will keep execution moving.
- When reporting visible reasoning, commands run, or local validation/test results, use one timestamp prefix per related block based on the current local shell time (for example `[$(date +"%Y-%m-%d %H:%M")]`) for traceability.
- If blocked, use:
  - `BLOCKER:` exact reason
  - `EVIDENCE:` file/command/error
  - `NEXT:` best next action

## References
- Docs hub: `docs/index.md`
- Codememory workflow: `docs/codememory-workflow.md`
- Codememory conventions: `docs/codememory-conventions.md`
- GitHub CLI patterns: `docs/github-cli.md`
- Validation gates and risk matrix: `docs/validation-policy.md`
- Quick commands: `docs/tooling-quick-ref.md`
- Advanced orchestration: `docs/orchestration-advanced.md`
