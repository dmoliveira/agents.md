# Agent Instructions

Use native repo tooling available in this environment (`git`, `gh`, `oc`, and built-in agent tools). Keep work scoped to one issue/task at a time.

## Quickstart
- Read `AGENTS.md`, pick one scoped issue/task, and execute in a dedicated worktree branch.
- Use the adaptive default loop: `resume -> classify -> research -> plan -> plan review -> define validation -> execute -> review/fix -> commit validated slice -> update Codememory -> continue/close`.
- Use `wt flow` for delivery work that should go through commit/PR/review/merge; never land feature changes directly on `main`.
- Keep issue/PR status updated through start, progress, and completion when GitHub tracking exists.
- Use `docs/tooling-quick-ref.md`, `docs/codememory-workflow.md`, `docs/codememory-conventions.md`, `docs/github-cli.md`, `docs/validation-policy.md`, and `docs/orchestration-advanced.md` as supporting references.
- Repo-root `AGENTS.md` is canonical. Runtime mirrors such as `my_opencode/AGENTS.md` SHOULD resolve to this file via symlink, not copy, so sandbox/runtime starts pick up the latest instructions from any launch location.

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
- For user-visible progress notes, command/test reporting, and rationale summaries, prefix each reporting block with a real local timestamp string collected from the shell at runtime (for example by running `date +"%Y-%m-%d %H:%M"` first and then pasting the resulting value in the format `[YYYY-MM-DD HH:MM]`) so execution traces are easier to follow without adding noise to every line. Do not print a literal shell expression such as `$(date ...)` in the response or reuse a canned sample timestamp.
- When a command/log/telemetry example includes the runtime session id, run `date +"%Y-%m-%dT%H:%M:%S%z"` first and include the rendered timestamp value with the session id so execution time is explicit and not auto-generated from memory. If you show shell syntax, keep it inside a code block or inline command example, not as the user-visible timestamp itself, and do not reuse placeholder values as if they were real output.
- Do not ask for confirmation unless ambiguity materially changes the result or a secret/credential is required.
- Do not hand low-impact decisions back to the user when the repo context already makes a reasonable choice clear; pick the strong default and keep moving.
- Treat naming, file placement, ordering, wording, and similarly small implementation details as agent-owned decisions unless the user explicitly asks to control them.
- Prefer making the next reasonable decision, documenting the rationale briefly, and advancing the task as far as safely possible in one run.
- Keep explanations lean; summarize long logs and keep evidence relevant.
- Default communication posture: low-token and high-signal. Keep routine progress, plan, and validation notes brief unless risk, ambiguity, or blockers require expansion.
- When a local OpenCode runtime such as `my_opencode` is available, inspect its capability/status commands before assuming optional workflows exist; for image/design work specifically, prefer `/image access --json`, `/image preference show --json`, and `/image location show --json` to discover the effective provider and artifact destination.
- When asked for the current runtime session id, output only the exact id from the session context and nothing else. Do not add acknowledgements, explanations, paraphrases, punctuation, or substitute another value.
- Check the remote state before starting implementation so the chosen task still matches the latest branch and PR state.
- Preserve user-authored changes when syncing or resolving conflicts in touched files.
- Keep implementations semantically structured; add comments only when they materially help.

## Default execution loop

### 1) Resume and align
1. Read `AGENTS.md`.
2. Fetch/check the remote so local context matches the latest branch and PR state.
3. Check Codememory startup context with `oc current`, `oc next`, `oc queue`, or `oc resume --task <id>` as appropriate.
4. Confirm the selected scope still fits the latest upstream branch state and does not duplicate overlapping in-flight work.
5. Create or attach the work to a Codememory `task` or `epic` before meaningful implementation continues.
6. Keep all meaningful execution in a dedicated worktree branch and bind the active Codememory session to that worktree.

### 2) Classify depth and risk
- Classify execution depth first:
  - `small`: clear low-blast-radius work; minimal research, micro-plan, one validation statement.
  - `medium`: typical feature/refactor/docs initiative spanning multiple files; explicit plan, plan review, named validation before coding.
  - `large`: cross-module, ambiguous, or dependency-heavy work; structured research, Codememory-backed sequencing/DAG, stronger validation plan.
- Classify delivery risk separately with the validation policy:
  - `low`: docs/tests/small scoped edit.
  - `medium`: typical feature/refactor.
  - `high`: runtime/security/migration or broad behavior change.

### 3) Research only to the depth needed
- Gather enough context to act safely, not a generic literature review.
- Research only the dimensions that matter for the slice: UX impact, acceptance/testing surface, implementation efficiency, modularity/extensibility, reusable local patterns, candidate libraries/tools, known issues, and key tradeoffs/pros-cons.
- Prefer local repo patterns first; use external research only when framework/library behavior materially affects the solution.

### 4) Plan, review the plan, and define validation before coding
- Turn research into a compact plan with the smallest useful execution slices.
- For `medium` and `large` work, review the plan before coding: challenge scope, sequencing, hidden dependencies, safer simpler paths, and rollback/containment where relevant.
- Define validation before implementation starts. Name the checks that prove done for the slice: docs checks, unit/integration tests, UX smoke paths, frontend/backend checks, sandbox/live-state runs, and debugging helpers such as Playwright/tmux/plain scripts when they improve confidence.
- Use Codememory to store the durable plan, dependencies, and validation definition whenever the task is meaningful or likely to resume.

### 5) Execute in validated slices
- Implement the smallest useful slice first.
- Keep local iteration fast; run lightweight checks only when they reduce risk or unblock debugging.
- Update the plan/Codememory when scope, decisions, blockers, or sequencing changes materially.

### 6) Review/fix/improve loop
- Run the required validation set for the current slice.
- Apply the risk-based review/fix budget from `docs/validation-policy.md`.
- Stop review cycling once required checks are green and the latest review has no blocker findings.
- Prefer one stronger realistic sandbox/live-state validation pass over many weak speculative checks when behavior matters.

### 7) Commit, continue, or deliver
- Commit only validated slices.
- Keep commit and push as separate steps for meaningful changes.
- If more in-scope slices remain, update Codememory with the current state and continue the loop.
- If the user asked for end-to-end delivery, continue into `wt flow` after the validated slice is ready.

## Delivery rules
- Any feature, improvement, or bug fix MUST use a dedicated worktree branch.
- Never repurpose `main` as a delivery branch; use `main` only for sync/merge.
- Prefer one focused commit per validated feature/task slice instead of many intermediate commits.
- Open a PR for delivery changes and merge to `main` only through the PR.
- When a user asks to do work "end-to-end", "e2e", or with equivalent shorthand, treat that as default authorization to run the full `wt flow` for the scoped request: split the work into focused validated slices when needed, commit the validated slice(s), open the PR, run the required risk-based review/fix/improve loop until the latest pass has no blocker findings, merge when checks are clear, delete the merged worktree/branch, and sync local `main`, unless the user explicitly narrows or overrides part of that flow.

## Codememory coordination
- Codememory is REQUIRED in this repo for internal execution tracking, handoffs, durable learnings, and resumable AI coordination.
- Treat Codememory as the source of truth for internal execution state; treat GitHub as the source of truth for delivery state, reviews, and merges.
- Use Codememory instead of ad hoc todo lists for meaningful work.
- Do not use OpenCode's `todowrite`/todo list for task coordination in this repo; use Codememory (`oc`) instead.
- Before starting or resuming meaningful work, check Codememory first with the startup flow in `docs/codememory-workflow.md`.
- Every meaningful request that creates work MUST create or attach to a Codememory `task` or `epic` before implementation continues.
- Every active implementation attempt MUST have a Codememory `session` tied to the active worktree path.
- Record durable blockers, decisions, ideas, assumptions, conventions, dependencies, and handoff context in Codememory so another AI can resume without relying on chat history.
- Keep Codememory-specific commands and conventions in the dedicated Codememory docs so future updates or temporary disablement stay localized.

## Validation and iterative testing
- Default to fast local iteration; avoid heavyweight checks on every edit.
- Define validation before coding and run the required gate once on the current full diff before claiming the slice is done.
- When the iterative-testing mode is `auto` or `on`, prefer a reproducible live-state check over guesswork for iterative or long-lived software flows. If terminal state is the blocker and `tmux` is available, inspect the running session there and send non-interactive commands instead of stopping at static analysis alone.
- Use `docs/validation-policy.md` for risk-based validation depth and `docs/iterative-testing-workflow.md` for live-state/sandbox rules.

## Concise communication module
- Repo mode for concise/terse communication guidance (for example via `/gateway concise` when the runtime provides it): `lite` by default; use `off`, `full`, or `ultra` only when the runtime or user explicitly enables or overrides them.
- Precedence: explicit user request > runtime/plugin mode > repo default behavior.
- When a concise mode is active, use `docs/concise-communication-workflow.md` and `skills/concise-mode/SKILL.md` so terse output stays technically accurate, easy to inspect via runtime status, and easy to disable.
- Relax concise mode for destructive warnings, ambiguity that requires clarity, and multi-step instructions where fragment-style wording would make the result less safe.

## Design/image workflow defaults
- When the task is concepting, visual exploration, or design-resource generation, use the repo-local design/image workflow instead of browser automation.
- In the `my_opencode` runtime, start with `/ox-design` for concept planning and `/image access --json` before assuming generation is available.
- If `/image access --json` reports a local Codex-backed path, agents MAY use that provider; if it is unavailable, fall back to the stable API-backed path or stay in prompt-only planning mode.
- Respect repo-local image output preferences so artifacts land where the operator expects; use `/image location show --json` when the destination matters.

## Orchestration quickplay
- Start in `build` for `small`, clear, single-scope changes.
- Switch to `orchestrator` when scope spans multiple files/modules, requires sequencing, or needs strict completion gates.
- Delegate intentionally: `explore` for discovery, `librarian` for external docs, `oracle` for hard tradeoffs, `verifier` for validation, `reviewer` for final risk review, `release-scribe` for PR/release text.
- Use Codememory-backed sequencing/DAG planning only when the work is `medium`/`large` enough that dependencies, parallelism, or resumability would otherwise get lost.
- Keep specialist subagents read-only and bounded; the primary agent integrates and lands changes.
- Browser-only blockers (OAuth consent, admin install/re-auth, scope upgrade prompts, final visual verification) should follow `docs/agent-browser.md` instead of stretching shell automation.
- Under pressure, reduce concurrency first and finish the active worktree card before opening another.

## `wt flow` delivery extension
1. Create a dedicated worktree and branch.
2. Fetch/check the remote branch state before implementation so the task starts from current upstream context.
3. Start or resume a Codememory session for that worktree and attach it to the active task.
4. Run the default execution loop until at least one validated slice is ready.
5. Create one focused commit for the validated slice.
6. Push the branch and open a PR.
7. Address review feedback and re-run checks only when needed.
8. Before merge, re-check `origin/main` plus overlapping PRs/branches for late conflicts or duplicated functionality.
9. Close the Codememory task/session state when the slice is done, failed, or canceled.
10. Merge when checks pass.
11. Delete the local worktree and branch.
12. Return to `main` and `git pull --rebase`.

## Project conventions
- Use `uv` for Python environments/dependencies and `ruff` for Python formatting/fixes.
- Prefer Makefiles for repeatable repo scripts; use `make help` first.
- Prefer running lint/tests at key gates instead of on every local iteration.
- If pre-commit is configured, use it at the pre-PR gate; if missing, installation is optional.
- Keep delivery documentation under `docs/`, with long-form planning docs organized by status under `docs/plan/{new,doing,blocked,parked,done,cancelled}` and specs in `docs/specs/`. Codememory remains the primary execution tracker.

## Final response pattern
- If work remains or a clear next execution step is already known: brief progress + blocker/next action + final line `<CONTINUE-LOOP>`.
- If work is complete: brief outcome + validation evidence + optional follow-up suggestions only when no further in-scope execution is pending.
- Use `<CONTINUE-LOOP>` whenever the task is not fully done and the next plan slice is already identifiable, even if the remaining work is small.
- Do not frame pending in-scope work as "best next steps" or optional suggestions; treat it as continuation and end with `<CONTINUE-LOOP>`.
- Do not ask the user to break ties between equivalent low-risk options when one reasonable default will keep execution moving.
- When reporting visible reasoning, commands run, or local validation/test results, use one timestamp prefix per related block based on the current local shell time (for example, after running `date +"%Y-%m-%d %H:%M"` in the shell first, prefix the block with the resulting value in the format `[YYYY-MM-DD HH:MM]`) for traceability. Do not print the literal command substitution form.
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
