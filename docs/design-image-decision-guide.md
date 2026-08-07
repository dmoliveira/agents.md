# Design image decision guide

Use this guide when a task touches UX visuals, design artifacts, or image generation.

## Use image/design generation when

- you are exploring concepts before implementation
- you need icons, palettes, wireframes, mockups, hero drafts, or typography directions
- a screenshot or product brief needs stronger visual directions
- the question is **what could this look like?**

## Use browser review when

- the UI already exists and needs verification
- you need responsive, accessibility, loading, empty, or error-state checks
- the task crosses a browser-owned boundary such as OAuth, install, re-auth, or scope acceptance
- the question is **how does the real thing behave?**

## Recommended split

- if you are using the `my_opencode` OpenCode runtime: concept and asset planning -> `/ox-design`
- if you are using the `my_opencode` OpenCode runtime: explicit OpenAI-backed artifact generation -> `/image`
- if you are using the `my_opencode` OpenCode runtime: real implemented UX review -> `/ox-ux`
- otherwise: use your repo-local design workflow for concepting/assets and keep browser usage scoped to implemented-UI validation or narrow browser-owned blockers

## Use the public `codex-image` CLI for portable API generation

Use [`codex-image`](https://github.com/dmoliveira/codex-image-cli) when an agent needs a documented, shell-only GPT Image 2 generation path that works outside a particular OpenCode runtime.

This is an **API-key-only** path:

- require `OPENAI_API_KEY` in the child-process environment
- do **not** reuse a ChatGPT/Codex subscription login, browser session, cookie, or access token
- treat a present key as local configuration only—not proof of billing, organization verification, model access, or entitlement
- never put the key in flags, prompts, URLs, JSON, files, or logs

Discover the installed contract and validate before any billable request:

```bash
codex-image ai-help --json
codex-image doctor --json

mkdir -p artifacts/design
codex-image generate \
  --prompt "<prompt>" \
  --output-dir artifacts/design \
  --prefix <safe-stem> \
  --n 1 \
  --dry-run \
  --json
```

Only after the dry run is correct, make one real request:

```bash
OPENAI_API_KEY="${OPENAI_API_KEY:?set in the environment}" \
codex-image generate \
  --prompt "<prompt>" \
  --output-dir artifacts/design \
  --prefix <safe-stem> \
  --n 1 \
  --json
```

`--output-dir` must already exist and have no symlinked path components. Use `--name` only for a single image; use `--prefix` for deterministic batches. Parse `outputs`, `retained_artifacts`, and `possibly_modified_paths` from JSON before cleanup. Never automatically retry exit codes `5`, `6`, or `7`: a generation may have been billed even without a usable image.

See [the dedicated agent protocol](codex-image-cli.md) for JSON/exit-code handling and the distinction from `my_opencode`'s experimental local providers.

## Artifact posture

When design outputs matter to delivery, keep them repo-native under:

```text
artifacts/design/
```

Commit curated assets when they materially help implementation, review, or communication.

## Runtime checks for agents

When `my_opencode` is available, agents should check the effective image workflow before generating assets:

```text
/image access --json
/image preference show --json
/image location show --json
```

Interpretation:

- `/image access --json` tells you whether the stable API-backed path and any experimental local Codex path are available.
- `/image preference show --json` tells you which provider will actually be used when the prompt does not pass `--provider`.
- `/image location show --json` tells you where generated artifacts will land by default.

Current local convention in `my_opencode` may prefer:

- provider: `codex-experimental`
- output location: `cwd-artifacts`

Agents should treat those as repo-local preferences, not universal defaults for every runtime.
