---
name: concise-mode
description: >
  Compact guidance for concise or caveman-style communication that reduces token usage
  while keeping technical accuracy. Supports off, lite, full, and ultra intensity levels.
---

Use this module when the user or runtime explicitly wants lower-token answers without losing technical substance. If the runtime exposes `/gateway concise status` or equivalent mode status, treat that as the canonical signal. Otherwise use the precedence and repo default defined in `AGENTS.md` and `docs/concise-communication-workflow.md`.

## Persistence

Active when the user or runtime enables it, or when the repo default applies. Precedence is explicit user request, then a valid runtime/plugin mode, then the repo default in `AGENTS.md`; missing or unknown mode falls back to that repo default, while explicit `off` remains authoritative. Some runtimes persist the chosen mode at repo scope until it changes or is turned off explicitly.

## Rules

- Remove filler, pleasantries, and weak hedging first.
- Keep technical terms, file paths, identifiers, commands, and exact errors unchanged.
- `lite`: concise but sentence-based.
- `full`: terse fragments OK when meaning stays obvious.
- `ultra`: strongest compression; use only when readability remains safe.
- Code blocks unchanged.

## Relax mode for clarity

Use fuller language for:

- destructive warnings
- security/privacy guidance
- multi-step procedures where order matters
- repeated confusion or explicit requests for more detail

## Pattern

Useful terse pattern:

- `[problem]. [cause]. [fix]. [next step].`

## Source of truth

For mode semantics, examples, and disable guidance, see `docs/concise-communication-workflow.md`.
