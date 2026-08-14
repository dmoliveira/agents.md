# Agent Instructions

Use native repo tooling (`git`, `gh`, `oc`, built-in agent tools); keep one scoped task active. Repo-root `AGENTS.md` is canonical; runtime mirrors SHOULD symlink to it rather than copy it.

## Authority and operating rules

- `MUST` is mandatory unless the user explicitly overrides it; `SHOULD` is the default; `MAY` is optional. Precedence: `AGENTS.md` > user request > general defaults. A *pending task* is uncompleted or unvalidated scope; a *blocker* prevents safe progress.
- Work autonomously: choose reasonable defaults, keep moving until done or concretely blocked, and ask only when ambiguity materially changes the result or requires a secret. Preserve user-authored changes while syncing/conflict-resolving.
- On resume, re-read this file and directly relevant workflow docs. Before implementation, fetch/check remote and GitHub state; confirm the scope is current and non-duplicative.
- Keep progress, rationale, commands, and validation high-signal. Prefix each user-visible reporting block with a freshly collected local `[YYYY-MM-DD HH:MM]` timestamp; never use a literal shell expression or canned timestamp. When showing a runtime session ID, include a freshly collected ISO timestamp; when asked for that ID, return only its exact value.
- When a local OpenCode runtime exists, inspect capability/status commands before assuming optional workflows are available.
- Keep always-on policy here; put bounded/domain procedures in skills. Use semantically structured implementations and comments only when they help.

## Execution lanes and authority

Classify the request before the first mutation. Start in the narrowest lane that fits and transition lanes explicitly when scope changes:

| Lane | May do | Must not do | Entry |
| --- | --- | --- | --- |
| **Read-only** | Inspect files, local state, SQLite, logs, branches, and remote metadata; analyze or review; delegate bounded discovery | Edit files, create worktrees/tasks/sessions, commit, push, open/merge PRs, or delete state | Default for research, audits, and review |
| **Implementation** | Edit the assigned worktree, run checks, fix findings, and create a focused validated local commit | Push, open/update PRs, merge, or delete branches/worktrees unless delivery is explicitly authorized | A clear implementation request plus the required task/session setup |
| **Delivery** | Push, open/update PRs, run review/fix, merge, clean up, and sync according to the requested flow | Exceed the requested repository/scope or bypass platform-required checks, reviews, or protections | An explicit delivery request or `e2e`/`end-to-end` authorization |

- Routine inspection, bounded delegation, implementation edits in the assigned worktree, validation, repair, and checkpoint commits do not need a separate human approval prompt. Continue autonomously while the next action is clear.
- Stop and ask only when ambiguity could materially change the result, a secret or browser-owned authorization is required, a security/privacy or irreversible-data risk appears, the request expands scope, a required check cannot be repaired safely within scope/budget, or delivery authorization is absent. A failed check is a repair signal first, not an approval boundary.
- `e2e`/`end-to-end` authorizes the delivery actions listed in the Delivery lane and `wt flow`; still report destructive actions, honor required platform checks/reviews, and abort on scope, authorization, or validation drift.

## Required lifecycle

1. **Align:** for read-only work, read instructions and inspect only the local state needed for the request; do not create tracking or delivery state. Before implementation or delivery, inspect remote/GitHub; run `oc current`, `oc next`, and `oc queue` (plus `oc resume` when resuming); use a dedicated worktree branch; create/attach the Codememory task, link a parent epic when needed, and bind its active session before the first edit. If Codememory is unavailable, follow the bounded outage path in `docs/codememory-workflow.md` and do not silently claim tracking.
2. **Classify:** depth is `small` (clear, low blast radius), `medium` (typical multi-file task), or `large` (cross-module, ambiguous, dependency-heavy). Risk is `low` (docs/tests/small edit), `medium` (feature/refactor), or `high` (runtime/security/migration/broad behavior).
3. **Research and plan:** research only what affects the slice, preferring local patterns. Define small slices and validation before coding. `medium`/`large` work needs plan review; `large` work needs durable Codememory sequencing/dependencies.
4. **Execute:** implement the smallest useful slice; iterate cheaply; record material decisions, blockers, assumptions, dependencies, or handoff context in Codememory.
5. **Validate and review:** run the named checks on the full diff, apply `docs/validation-policy.md` risk budget, fix and rerun failed checks autonomously, and stop only when checks are green and the latest review has no blocker. Prefer realistic live-state validation when behavior matters.
6. **Deliver:** commit only validated slices; separate meaningful commits from pushes; update Codememory when continuing or closing. Use `wt flow` after a validated slice for end-to-end work.

## Delivery and Codememory invariants

- Features, improvements, and fixes MUST use a dedicated worktree; never deliver from `main`. Use a focused validated commit, PR-only merge, and current issue/PR status when tracking exists.
- “End-to-end”/“e2e” authorizes the full `wt flow`: worktree + current upstream/Codememory session, validated slice, commit/push/PR, review/fix, recheck `origin/main` and overlaps, merge, close Codememory state, delete branch/worktree, and `main` rebase-sync.
- Codememory is REQUIRED for implementation/delivery execution and handoffs; read-only discovery is the intentional exception. GitHub is authoritative for delivery/reviews/merges. Do not use `todowrite` or ad hoc task lists. Every implementation attempt needs a Codememory task (linked to an epic when applicable) and a session tied to its worktree. If the configured Codememory backend is unhealthy, run one bounded diagnosis, preserve the exact error, and stop before new implementation/delivery unless the user explicitly overrides the tracking requirement; if it fails mid-slice, freeze the diff and follow the read-only diagnostic path in `docs/codememory-workflow.md`. See that workflow and `docs/codememory-conventions.md` for commands and recovery.

## Validation and routing

- Start with the smallest appropriate validation bundle: docs/config/skills usually `git diff --check`; Python edits also `python3 -m py_compile <touched-files>`; broaden for risk/surface. Use `docs/validation-policy.md`; use reproducible live-state checks and `tmux` inspection in iterative `auto`/`on` flows when static checks are insufficient.
- Default concise mode is `lite`; precedence is explicit user request > runtime/plugin mode > repo default. Follow `docs/concise-communication-workflow.md` and `skills/concise-mode/SKILL.md`; relax compression for destructive warnings, material ambiguity, or unsafe multi-step instructions.
- For design/image work, use the repo design workflow, `/ox-design`, then `/image access --json`; inspect preference/location when relevant. For a portable public API CLI, use the `codex-image` protocol in `docs/codex-image-cli.md`—it requires `OPENAI_API_KEY`, not a ChatGPT/Codex subscription credential. Browser-only auth/admin/final-visual blockers follow `docs/agent-browser.md`.
- Use `build` for small clear work and `orchestrator` for multi-file/sequenced work. Delegate bounded work with the packet in `docs/orchestration-advanced.md`; default workers to read-only. An implementation packet must name the owned worktree/paths, allowed mutations, prohibited delivery actions, acceptance criteria, stop conditions, checks, and return evidence. Workers never push, merge, delete branches/worktrees, alter coordinator state, or expand scope unless the packet explicitly authorizes the narrower action. Delegate bounded read-only work: `explore` (discovery), `librarian` (external docs), `oracle` (hard tradeoffs), `verifier` (validation), `reviewer` (final risk), `release-scribe` (release text). Do not duplicate verifier/reviewer passes without changed evidence; reduce concurrency before opening more worktrees.

## Project conventions

- Use `uv` and `ruff` for Python. Prefer Makefiles; run `make help` first. Run lint/tests at gates; use configured pre-commit before PRs.
- Put delivery docs under `docs/`; place plans in `docs/plan/{new,doing,blocked,parked,done,cancelled}` and specs in `docs/specs/`.

## Response contract

- If work remains and the next action is clear, continue autonomously instead of asking the user to continue. Emit `<CONTINUE-LOOP>` only when the runtime requires a new turn or work is intentionally paused; include the next action and any real blocker, never a routine approval request.
- If complete, report outcome and validation evidence. Do not hand equivalent low-risk choices back to the user.
- If blocked, use `BLOCKER:`, `EVIDENCE:`, and `NEXT:` with the exact reason, evidence, and best action.

## References

- `docs/index.md`, `docs/tooling-quick-ref.md`, `docs/codememory-workflow.md`, `docs/codememory-conventions.md`, `docs/github-cli.md`
- `docs/validation-policy.md`, `docs/iterative-testing-workflow.md`, `docs/orchestration-advanced.md`
