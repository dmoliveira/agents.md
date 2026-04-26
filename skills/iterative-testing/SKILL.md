---
name: iterative-testing
description: >
  Compact guidance for validating iterative, stateful, or live-runtime software flows.
  Use when confidence depends on current session state, a running process, or one stronger sandbox pass.
---

Use this repo-local module when static inspection plus ordinary lint/unit checks are not enough to trust the actual behavior. It is most relevant when the repo iterative-testing mode is `auto` or `on`.

## Trigger

Use when one or more are true:

- current CLI/TUI/runtime state is where the behavior appears
- the process must stay running to observe the issue or confirm the fix
- the change is important or behavior-heavy enough to justify one realistic sandbox pass

## Core rules

- Prefer live-state validation over guesswork when the failure only appears in the running process.
- If terminal/session state is the blocker and `tmux` is available, use it to inspect live output and send non-interactive commands into the running session.
- For important or behavior-heavy changes, add one best-available sandbox validation pass that exercises real behavior in isolation.
- Keep the workflow proportional: one stronger realistic check is better than many weak speculative ones.

## Boundaries

- Keep standard lint/test/build gates; this module supplements them.
- Do not use browser automation when shell-side live-state inspection is enough.
- If the blocker is browser-owned state, use `docs/agent-browser.md` instead.
- Keep commands reproducible and non-interactive.

## Evidence

Record the runtime or sandbox used, the key command(s), and the observed result.

## Source of truth

For full operational detail, mode semantics, and disable guidance, see `docs/iterative-testing-workflow.md`.
