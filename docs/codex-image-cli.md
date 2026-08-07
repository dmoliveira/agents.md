# `codex-image` CLI protocol 🖼️

Use this protocol when an agent needs portable, non-interactive GPT Image 2 generation through the public [`codex-image-cli`](https://github.com/dmoliveira/codex-image-cli) Rust binary.

## Account and credential boundary 🔐

`codex-image` calls the documented OpenAI Image API with `OPENAI_API_KEY` only.

- ChatGPT/Codex subscriptions and API billing are separate.
- Do not reuse browser cookies, Codex login state, OAuth tokens, or subscription credentials.
- `codex-image doctor --json` reports only local key presence. It does not remotely authenticate, verify billing, or prove model entitlement.
- Never pass a key in flags, prompts, URLs, JSON, source files, screenshots, or logs.

This is intentionally different from a repo-local `my_opencode` experimental provider such as `codex-experimental`; do not treat their authentication behavior as interchangeable.

## Non-interactive agent recipe 🤖

```bash
# Read the installed machine contract. No request is sent.
codex-image ai-help --json
codex-image doctor --json

# Create a project-owned destination, then validate without a key/network/file reservation.
mkdir -p artifacts/design
codex-image generate \
  --prompt "<prompt>" \
  --output-dir artifacts/design \
  --prefix <safe-stem> \
  --n 1 \
  --dry-run \
  --json

# Make exactly one billable request only after the dry run is accepted.
OPENAI_API_KEY="${OPENAI_API_KEY:?set in the environment}" \
codex-image generate \
  --prompt "<prompt>" \
  --output-dir artifacts/design \
  --prefix <safe-stem> \
  --n 1 \
  --json
```

Inputs never arrive from interactive stdin. Use `--prompt` or an existing UTF-8 `--prompt-file`; `--prompt-file -` is rejected to prevent blocking. A safe stem is 1–80 ASCII letters/digits/`_`/`-`, beginning with a letter or digit.

## JSON handling and cost safety 🧯

Always use `--json` and parse one JSON object from stdout:

| Field | Agent handling |
| --- | --- |
| `ok`, `status`, `exit_code` | Decide whether the command completed; do not infer success from process output alone. |
| `outputs` | Consume only after `ok: true`. |
| `retained_artifacts` | A successful overwrite can retain an identity-checked private backup; do not delete it automatically. |
| `possibly_modified_paths` | Inspect before any cleanup or retry after an error. |
| `request.request_id` | Preserve for an operator; it is safe/redacted by the CLI. |

Exit codes `5`, `6`, and `7` are **not safe to retry automatically**. The POST may have been accepted/billed even if transport, response validation, or output publication failed. Report the JSON record and let the caller decide after checking API activity.

## Output and endpoint safety 📁

- Create `--output-dir` explicitly. On supported macOS/Linux generation paths, it must be an existing directory without symlinked components; unsupported platforms fail closed before an API request.
- Use `--name` only with `--n 1`; use `--prefix` for multi-image names such as `hero-01.png`.
- `--dry-run` reads no key, reserves no files, and makes no DNS/proxy/HTTP call.
- Do not set `--api-base-url` in routine production use. Loopback HTTP needs `--allow-insecure-localhost`; a non-loopback custom HTTPS endpoint additionally needs an exact `--dangerously-allow-api-key-to` acknowledgement.
- Never ask the CLI to clean hidden transaction artifacts automatically in a concurrently writable directory.

For the full wire/exit contract, defer to the installed repository's `docs/API-CONTRACT.md` and `AGENTS.md`.
