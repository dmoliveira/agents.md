# Concise Communication Workflow

Use this optional module when the user or runtime wants lower-token, higher-density answers without losing technical accuracy. One runtime surface may expose it as `/gateway concise ...`.

## Mode model

- `off`: normal repo communication style.
- `lite`: remove filler and hedging, but keep normal sentence structure.
- `full`: prefer short direct fragments, drop filler words and most articles, keep technical terms exact.
- `ultra`: maximize compression while preserving correctness; use only when readability remains safe.

The runtime MAY expose independent submodes such as `review`, `commit`, or `compress`. Treat them as concise-output variants, not as replacements for correctness or validation. Missing or unknown runtime mode means `off`.

## Precedence

1. explicit user request
2. runtime/plugin mode
3. repo default in `AGENTS.md`

## Canonical runtime signal

If a runtime exposes concise-mode controls, treat its effective-mode status output (for example `/gateway concise status` or equivalent gateway state) as the source of truth. Missing or unknown mode means `off`.

## Core rules

- Preserve technical substance; remove fluff.
- Keep code blocks, commands, identifiers, filenames, flags, and exact errors unchanged.
- Prefer concrete nouns and verbs over polite filler.
- Short fragments are acceptable when the meaning stays obvious.
- If a short answer becomes ambiguous, expand enough to keep the meaning safe.

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

- Do not compress away critical risk, blocker, or validation evidence.
- Do not rewrite code style inside code blocks just to sound terse.
- Do not force concise mode on every repo or every session.
- Keep the module easy to disable or override.

## Temporary disable path

To disable this module with minimal churn:

1. remove or change the concise communication section in `AGENTS.md`
2. remove the short references in `docs/index.md` and `docs/tooling-quick-ref.md`
3. remove the concise module inventory entry from `skills/README.md`
4. keep this file and `skills/concise-mode/SKILL.md` as archival docs or delete them together

This separation is intentional so runtime plugins can consume the concise-mode contract without hardwiring it into all sessions.
