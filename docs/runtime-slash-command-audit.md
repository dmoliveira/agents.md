# Runtime Slash Command Audit

Use this runbook when you need to validate that high-value OpenCode slash commands are reading the right repo/runtime context instead of relying on stale or hardcoded assumptions.

## What to test first

Rank commands by impact and dynamic-context risk:

1. `auto-slash`
   - routes natural language into other commands
   - failures here fan out into wrong command selection
2. `gateway concise`
   - should reflect the current runtime session and effective concise-mode status
3. `image`
   - should resolve provider and output preferences from the active repo context
4. `session`
   - should report the active runtime session id and cwd accurately
5. `workflow`
   - should expose current workflow/task-graph state and at least sanity-check idle versus running state
6. `delivery`
   - depends on workflow, governance, and task state
7. `ox-*`
   - important after route quality is trusted because `auto-slash` may hand work to them

## Fast audit command

Run from the repo you want to validate:

```bash
python3 scripts/slash_command_audit.py --json
```

The harness seeds its own audit session id when `OPENCODE_SESSION_ID` is not already set, so it remains runnable as a standalone repo check.

Or use the Make target:

```bash
make slash-audit
```

The audit script checks:

- configured slash-command inventory from `my_opencode/opencode.json`
- `auto-slash` route quality for representative prompts
- `gateway concise status --json` session-awareness, with the full status payload available for manual inspection
- `image preference/location/access --json` repo-context resolution
- `digest run --reason manual`, then `session current --json` and `session handoff --json` lifecycle assertions
- `workflow status --json` idle/running state reporting

## What counts as a good result

- `auto-slash` matches strong intent prompts and avoids meta/no-op prompts
- `gateway concise status` reports the current `OPENCODE_SESSION_ID`, while effective mode/source fields remain visible in the captured payload
- `image` preference files resolve from the repo being audited, not an unrelated checkout
- after a refreshed digest, `session current` and `session handoff` both point back to the current repo/session
- `workflow status` reports a sane idle/running status value for the current runtime state

## When to use `tmux`

Use `tmux` only when a one-shot command is not enough to inspect live runtime state.

Good uses:

- validating a long-running runtime session
- checking state that changes during a multi-step command flow
- observing live output before and after a slash command mutates runtime state

Skip `tmux` for simple read-only status checks that already return enough evidence directly.

## Typical failure patterns worth capturing

- route misses on high-value `auto-slash` prompts such as design/review/ship intents
- built-in command doctor passing even though important intents are untested
- file-backed image preference paths resolving from the runtime repo instead of the active repo
- session lifecycle only working after a digest refresh, or still failing even after digest/index state is written

When these appear, capture the durable finding in Codememory and decide whether the fix belongs in this repo (guidance/runbook/test harness) or in the runtime implementation.
