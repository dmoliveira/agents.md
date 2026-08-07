# Agent Instructions

Use native repo tooling (`git`, `gh`, `oc`, built-in agent tools); keep one scoped task active. Repo-root `AGENTS.md` is canonical; runtime mirrors SHOULD symlink to it rather than copy it.

## Authority and operating rules

- `MUST` is mandatory unless the user explicitly overrides it; `SHOULD` is the default; `MAY` is optional. Precedence: `AGENTS.md` > user request > general defaults. A *pending task* is uncompleted or unvalidated scope; a *blocker* prevents safe progress.
- Work autonomously: choose reasonable defaults, keep moving until done or concretely blocked, and ask only when ambiguity materially changes the result or requires a secret. Preserve user-authored changes while syncing/conflict-resolving.
- On resume, re-read this file and directly relevant workflow docs. Before implementation, fetch/check remote and GitHub state; confirm the scope is current and non-duplicative.
- Keep progress, rationale, commands, and validation high-signal. Prefix each user-visible reporting block with a freshly collected local `[YYYY-MM-DD HH:MM]` timestamp; never use a literal shell expression or canned timestamp. When showing a runtime session ID, include a freshly collected ISO timestamp; when asked for that ID, return only its exact value.
- When a local OpenCode runtime exists, inspect capability/status commands before assuming optional workflows are available.
- Keep always-on policy here; put bounded/domain procedures in skills. Use semantically structured implementations and comments only when they help.

## Required lifecycle

1. **Align:** read instructions; inspect remote/GitHub; run `oc current`, `oc next`, and `oc queue` (plus `oc resume` when resuming); use a dedicated worktree branch; create/attach the Codememory task, link a parent epic when needed, and bind its active session before meaningful implementation.
2. **Classify:** depth is `small` (clear, low blast radius), `medium` (typical multi-file task), or `large` (cross-module, ambiguous, dependency-heavy). Risk is `low` (docs/tests/small edit), `medium` (feature/refactor), or `high` (runtime/security/migration/broad behavior).
3. **Research and plan:** research only what affects the slice, preferring local patterns. Define small slices and validation before coding. `medium`/`large` work needs plan review; `large` work needs durable Codememory sequencing/dependencies.
4. **Execute:** implement the smallest useful slice; iterate cheaply; record material decisions, blockers, assumptions, dependencies, or handoff context in Codememory.
5. **Validate and review:** run the named checks on the full diff, apply `docs/validation-policy.md` risk budget, fix findings, and stop only when checks are green and the latest review has no blocker. Prefer realistic live-state validation when behavior matters.
6. **Deliver:** commit only validated slices; separate meaningful commits from pushes; update Codememory when continuing or closing. Use `wt flow` after a validated slice for end-to-end work.

## Delivery and Codememory invariants

- Features, improvements, and fixes MUST use a dedicated worktree; never deliver from `main`. Use a focused validated commit, PR-only merge, and current issue/PR status when tracking exists.
- “End-to-end”/“e2e” authorizes the full `wt flow`: worktree + current upstream/Codememory session, validated slice, commit/push/PR, review/fix, recheck `origin/main` and overlaps, merge, close Codememory state, delete branch/worktree, and `main` rebase-sync.
- Codememory is REQUIRED for internal execution/handoffs; GitHub is authoritative for delivery/reviews/merges. Do not use `todowrite` or ad hoc task lists. Every meaningful task needs a Codememory task (linked to an epic when applicable); every implementation attempt needs a session tied to its worktree. See `docs/codememory-workflow.md` and `docs/codememory-conventions.md` for commands and recovery.

## Validation and routing

- Start with the smallest appropriate validation bundle: docs/config/skills usually `git diff --check`; Python edits also `python3 -m py_compile <touched-files>`; broaden for risk/surface. Use `docs/validation-policy.md`; use reproducible live-state checks and `tmux` inspection in iterative `auto`/`on` flows when static checks are insufficient.
- Default concise mode is `lite`; precedence is explicit user request > runtime/plugin mode > repo default. Follow `docs/concise-communication-workflow.md` and `skills/concise-mode/SKILL.md`; relax compression for destructive warnings, material ambiguity, or unsafe multi-step instructions.
- For design/image work, use the repo design workflow, `/ox-design`, then `/image access --json`; inspect preference/location when relevant. For a portable public API CLI, use the `codex-image` protocol in `docs/codex-image-cli.md`—it requires `OPENAI_API_KEY`, not a ChatGPT/Codex subscription credential. Browser-only auth/admin/final-visual blockers follow `docs/agent-browser.md`.
- Use `build` for small clear work and `orchestrator` for multi-file/sequenced work. Delegate bounded read-only work: `explore` (discovery), `librarian` (external docs), `oracle` (hard tradeoffs), `verifier` (validation), `reviewer` (final risk), `release-scribe` (release text). Do not duplicate verifier/reviewer passes without changed evidence; reduce concurrency before opening more worktrees.

## Project conventions

- Use `uv` and `ruff` for Python. Prefer Makefiles; run `make help` first. Run lint/tests at gates; use configured pre-commit before PRs.
- Put delivery docs under `docs/`; place plans in `docs/plan/{new,doing,blocked,parked,done,cancelled}` and specs in `docs/specs/`.

## Response contract

- If work remains and the next action is clear, report brief progress plus blocker/next action and end with `<CONTINUE-LOOP>`; do not present pending work as optional.
- If complete, report outcome and validation evidence. Do not hand equivalent low-risk choices back to the user.
- If blocked, use `BLOCKER:`, `EVIDENCE:`, and `NEXT:` with the exact reason, evidence, and best action.

## References

- `docs/index.md`, `docs/tooling-quick-ref.md`, `docs/codememory-workflow.md`, `docs/codememory-conventions.md`, `docs/github-cli.md`
- `docs/validation-policy.md`, `docs/iterative-testing-workflow.md`, `docs/orchestration-advanced.md`
