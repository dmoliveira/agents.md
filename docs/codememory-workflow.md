# Codememory Workflow

Use this as the required Codememory operating flow for this repo.

GitHub remains the external delivery tracker.
Codememory is the internal execution tracker and handoff memory.

## Why this exists

- keep AI execution resumable across context compression and handoffs
- replace ad hoc todo lists, including OpenCode's `todowrite`/todo list, with durable repo-scoped state
- keep branch/worktree execution tied to explicit task and session records
- centralize Codememory instructions so future updates or temporary disablement stay localized

## Repo defaults

- default repo `scope_key`: use the GitHub repo slug for this repo
- use one active Codememory session per active worktree path
- use one active Codememory task per focused execution slice
- use GitHub Issues/PRs for delivery visibility; do not use them as the only AI handoff medium
- prefer a repo-local `.codememory/config.yaml` that sets `defaults.scope_key` to the repo slug; until that exists, pass `--scope <repo-scope>` explicitly on Codememory reads and writes

## Execution lanes

`AGENTS.md` owns lanes and authority. This page owns Codememory commands, tracking, recovery, and closeout; read-only work and the documented outage fallback are exceptions to tracked startup. Delegated workers are read-only unless their packet grants bounded implementation scope.

## Required startup flow

Before meaningful work begins:

1. Read `AGENTS.md`.
2. For implementation or delivery, check remote and GitHub state. For read-only discovery, skip remote mutation and inspect only the local state needed for the request.
3. For implementation or delivery, check Codememory state for the repo:
   - `oc current`
   - `oc next --scope <repo-scope> --limit 5`
   - `oc queue --scope <repo-scope> --limit 10`
4. If resuming a known task, run:
   - `oc resume --scope <repo-scope> --task <task_id>`
5. If the request creates new work, create or attach a Codememory `task` before implementation; for a broader initiative, create an `epic` and link the task to it.
6. For non-trivial implementation or delivery, capture the execution depth, plan slice, and validation definition before coding.

If `oc current` or `oc resume` shows a valid active session bound to the current worktree, continue that flow instead of opening a parallel duplicate.

### Transient Codememory outage

When an `oc` command fails because the configured backend is unavailable or unhealthy:

1. Run one bounded `oc config --doctor` diagnosis and preserve the exact command and error.
2. Do not repeatedly retry, reset a database, rewrite configuration, switch backends, or delete state automatically.
3. Read-only discovery may continue and report its evidence.
4. For **small/medium-depth, low/medium-risk** implementation, continue the bounded local slice in its dedicated worktree, run its validation, and optionally create the focused local commit. Mark the run `tracking-incomplete`; do not push, open/update a PR, merge, delete state, or claim durable Codememory state.
5. For **large-depth or high-risk** work, stop with `BLOCKER:`, `EVIDENCE:`, and `NEXT:` before new mutations.

If the outage appears after implementation has already started, only a **small/medium-depth, low/medium-risk** slice may finish its existing bounded work and validation; do not broaden scope or start a new slice. Large-depth or high-risk work freezes before further mutation and reports `BLOCKER:`, `EVIDENCE:`, and `NEXT:`. A focused local commit is allowed after eligible work validates, but no push, PR, merge, cleanup, or other remote mutation is allowed until tracking is restored.

Before any later push, PR, or merge, restore the backend and reconcile the task, session, changed files, local commit, and outcome in Codememory. Delivery remains subject to repository/platform-required checks and protections.

This transient-outage path is distinct from the intentional temporary disable path below.

## Required intake flow

Use single commands first.

### New actionable work

- create a task: `oc add task "<title>" ...`
- create an epic when the work spans multiple tasks: `oc add epic "<title>" ...`
- link a task to its epic when needed: `oc link <epic_id> parent-of <task_id>`

### Durable ideas or improvements

- `oc report improvement "<title>" --body "<context>" ...`

### Durable problems or blockers

- `oc report error "<title>" --body "<context>" ...`

### Durable rules, decisions, assumptions, conventions

- `oc add memory "<title>" --kind decision|constraint|assumption|convention ...`

### Richer repo or external references

- `oc add doc "<title>" --type repo_md|local_file|remote_url|design_note|runbook ...`

## Worktree flow

1. Create or resume the Git worktree branch.
2. When Codememory is available, start a session with `oc add session "<title>" --worktree . --task <task_id> ...`, or resume the matching session, bound to that worktree path. During the bounded outage fallback, keep the dedicated worktree and mark tracking as incomplete instead.
3. When tracked, ensure the session is attached to the active task and, when applicable, that task is linked to its parent epic.
4. Capture the durable execution brief before coding when the slice is meaningful:
   - current objective
   - chosen approach or options under consideration
   - dependencies/sequence if the work is `medium` or `large`
   - validation definition for the slice
5. Implement in that worktree.
6. Record durable execution state in Codememory when available and when decisions, blockers, assumptions, sequencing, or parent-epic progress change materially. In fallback mode, preserve the same evidence in the run report and reconcile it before remote delivery.
7. Validate.
8. When tracked, close the session and task state when the slice outcome is known; in fallback mode, report the untracked outcome and reconcile before remote delivery.

## Recommended capture shape by execution phase

### Research
- Capture only durable findings that affect future execution: chosen pattern, relevant dependency behavior, UX/testing constraints, or library/tool decisions.

### Plan
- Record the smallest useful slices, major dependencies, and any parallelizable work worth preserving across handoffs.
- For `large` work, use Codememory to preserve the execution graph/DAG logic so another AI can resume sequencing without rebuilding it from chat history.

### Plan review
- Record only the durable outcome: scope reduced, approach changed, dependency uncovered, or rollback/containment requirement added.

### Validation definition
- Record the slice checks; use `docs/validation-policy.md` for the gate and review budget.

### Execution/review loop
- Update Codememory when the plan changes, a blocker appears, or a completed slice changes the next best action.

## During execution

Write to Codememory when the information would matter after chat history is compressed or another AI takes over.

Capture at least these when they appear:

- new durable blocker
- decision that changes execution or architecture
- user preference likely to matter later
- reusable convention or assumption
- idea worth revisiting later
- important handoff context

Do not spam Codememory with every transient note. Prefer durable and resumable state over minute-by-minute logs.

## Closeout flow

Before ending a meaningful task slice:

1. update Codememory task state with the latest validated outcome; update its parent epic when the slice changes initiative progress
2. record any durable learnings, blockers, dependencies, or next-slice context
3. close the Codememory session with the correct outcome when the session is actually ending
4. update GitHub issue/PR state when default delivery is in scope or e2e is explicitly requested
5. continue the next slice automatically within the default delivery scope; an explicit local-only boundary ends the slice after its validated commit, and merges still go through the protected Delivery workflow

Typical commands:

- task complete: `oc done <task_id> --note "<result>"`
- task failed: `oc fail <task_id> --why "<reason>"`
- task canceled: `oc cancel <task_id> --why "<reason>"`
- session end: `oc end-session <session_id> --outcome done|failed|canceled`

## Recovery and AI handoff

When taking over from another AI or after context compression:

1. read `AGENTS.md`
2. run `oc current`
3. run `oc next --scope <repo-scope> --limit 5` and `oc queue --scope <repo-scope> --limit 10`
4. run `oc resume --scope <repo-scope> --task <task_id>` for the intended slice
5. read any linked docs only after Codememory narrows the active context

Prefer Codememory recovery over rereading large chat histories.

## Worktree and branch reuse policy

Reuse an existing worktree or branch only when all are true:

- the task is still active and still the intended slice
- the branch is not merged
- the worktree is safe to continue
- the Codememory session/task context still matches reality

Create a fresh worktree or branch when any of these are true:

- the previous branch already merged
- the task scope changed materially
- the prior session is stale or misleading
- branch drift or conflict makes continuation risky

When in doubt, prefer a fresh worktree and a fresh session while keeping the same repo `scope_key` and task linkage.

## Temporary disable path

If Codememory must be temporarily disabled later, keep the rollback localized:

1. update the Codememory section in `AGENTS.md`
2. remove Codememory references from `docs/index.md` and `docs/tooling-quick-ref.md`
3. preserve the GitHub/worktree flow unchanged

This separation is intentional so Codememory policy can evolve without rewriting the rest of the repo workflow.
