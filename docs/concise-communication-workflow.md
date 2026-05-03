# Concise Communication Workflow

Use this module when the user, runtime, or repo default wants lower-token, higher-density answers without losing technical accuracy. One runtime surface may expose it as `/gateway concise ...`.

## Mode model

- `off`: normal repo communication style.
- `lite`: remove filler and hedging, but keep normal sentence structure.
- `full`: prefer short direct fragments, drop filler words and most articles, keep technical terms exact.
- `ultra`: maximize compression while preserving correctness; use only when readability remains safe.

The runtime MAY expose independent submodes such as `review`, `commit`, or `compress`. Treat them as concise-output variants, not as replacements for correctness or validation. Missing or unknown runtime mode means: fall back to the repo default from `AGENTS.md` unless the user explicitly asked for `off`.

## Runtime taxonomy

Use this split when a runtime exposes concise controls:

| Category | Examples | Persistence | Notes |
|---|---|---|---|
| Repo default | `off`, `lite`, `full`, `ultra` | repo-scoped | Default for future sessions in that repo when the runtime supports it. This repo currently defaults to `lite` in `AGENTS.md`. |
| Active session mode | `lite`, `full`, `ultra`, `review`, `commit` | session-scoped | Applies to the current runtime session only unless changed again. |
| One-shot alias | `compress` | one-shot | Runs a related low-token or cleanup action without becoming the active communication mode. |

If a runtime uses different names, keep the behavior split the same: durable defaults, session-scoped active mode, and one-shot aliases.

## Precedence

1. explicit user request
2. runtime/plugin mode
3. repo default in `AGENTS.md`

## Canonical runtime signal

If a runtime exposes concise-mode controls, treat its effective-mode status output (for example `/gateway concise status` or equivalent gateway state) as the source of truth. Missing or unknown mode means: fall back to the repo default in `AGENTS.md`.

## Core rules

- Preserve technical substance; remove fluff.
- Keep code blocks, commands, identifiers, filenames, flags, and exact errors unchanged.
- Prefer concrete nouns and verbs over polite filler.
- Short fragments are acceptable when the meaning stays obvious.
- If a short answer becomes ambiguous, expand enough to keep the meaning safe.
- Do not compress away plan-review outcomes, validation definitions, blocker evidence, or final state.

## Safe compression targets

Good candidates for concise mode:

- direct debugging explanations
- validation summaries
- commit/review suggestions
- PR summaries and release notes
- routine operational updates

## When to relax or disable concise mode

Return to normal clarity for:

- destructive or irreversible warnings
- security/privacy guidance where nuance matters
- multi-step instructions where compressed wording could reorder meaning
- repeated confusion from the user
- situations where the user explicitly asks for fuller explanation

## Examples

Normal:

> The issue is likely caused by creating a new object reference during every render. Because React compares props shallowly, the inline object looks different each time and triggers another render.

Concise (`full`):

> New object ref each render. Inline prop fails shallow compare. React re-renders.

Normal:

> I ran the required checks and everything passed successfully. The branch is ready for a pull request.

Concise (`lite`):

> Checks passed. Branch ready for PR.

## Boundaries

- Do not compress away critical risk, blocker, validation evidence, plan-review outcome, or validation definition.
- Do not rewrite code style inside code blocks just to sound terse.
- Do not force stronger concise modes on every repo or every session; keep `off` and `lite` easy to choose.
- Keep the module easy to disable or override.

## Temporary disable path

To disable this module with minimal churn:

1. remove or change the concise communication section in `AGENTS.md`
2. remove the short references in `docs/index.md` and `docs/tooling-quick-ref.md`
3. remove the concise module inventory entry from `skills/README.md`
4. keep this file and `skills/concise-mode/SKILL.md` as archival docs or delete them together

This separation is intentional so runtime plugins can consume the concise-mode contract without hardwiring it into all sessions.
