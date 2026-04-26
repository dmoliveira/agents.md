# Iterative Testing Workflow

Use this optional module for software/products where confidence depends on current runtime state, session state, or a realistic isolated environment rather than static code inspection alone.

## Mode model

- `off`: do not apply this workflow by default unless the user explicitly asks for it.
- `auto`: apply it when the task is stateful or iterative and the relevant tooling/runtime is available.
- `on`: treat it as standard validation guidance for applicable tasks.

Mode precedence:

1. explicit user request
2. repo mode in `AGENTS.md`
3. default behavior

## When to use this workflow

Use it when one or more are true:

- the bug or feature depends on current CLI/TUI/app state
- the fastest trustworthy signal comes from observing a running process
- unit/lint/static checks are necessary but not sufficient
- the change is important or behavior-heavy enough to justify one stronger sandbox pass

## Live-state validation

Prefer live-state validation when failures surface in the running process rather than in source text.

Examples:

- multi-step CLI flows
- TUI navigation or prompts
- long-running daemons or watchers
- stateful local apps where process output changes over time

Use a quick smoke path first, then broaden only if confidence is still low.

## `tmux` guidance

If current terminal/session state is the blocker and `tmux` is available:

- inspect the live pane instead of restarting blindly
- keep the relevant process attached to a named session
- send non-interactive commands into the running session when needed
- prefer stable descriptive session names such as `ai-oc-<task>`

Use `tmux` when it improves observability. Do not add it to simple one-shot command flows that are already easy to observe directly.

## Sandbox validation

For important or behavior-heavy changes, add one best-available sandbox validation pass that exercises real behavior in isolation.

Good sandbox examples:

- disposable temp workspace
- seeded local app instance
- ephemeral test database or service container
- isolated config/profile directory
- dedicated worktree with realistic startup commands

Prefer the strongest realistic isolated environment available without turning a normal task into a heavyweight lab exercise.

## Boundaries

- Do not replace core lint/test/build checks with this workflow; add it when it materially improves confidence.
- Do not use browser automation when shell-side live-state inspection is sufficient.
- If the blocker is truly browser-owned state, switch to `docs/agent-browser.md`.
- Keep commands non-interactive and reproducible.

## Evidence to record

When this workflow is used for meaningful work, record:

- the runtime or sandbox path used
- the key command(s) run
- the observed result that increased confidence

Summarize this evidence in the final validation note or PR description. When the task is meaningful, also capture durable iterative-testing findings in Codememory.

## Temporary disable path

To disable this module with minimal churn:

1. remove or change the iterative-testing mode section in `AGENTS.md`
2. remove the short references in `docs/validation-policy.md`, `docs/index.md`, and `docs/tooling-quick-ref.md`
3. keep this file and `skills/iterative-testing/SKILL.md` as archival docs or delete them together

This separation is intentional so the iterative-testing policy can evolve without rewriting the rest of the repo workflow.
