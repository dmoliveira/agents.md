# Release Notes Template

Use this lightweight template for repo release notes, milestone notes, or PR rollups that need a clear user-facing summary.

## Style goals

- Keep it concise, friendly, and easy to scan.
- Use smart, plain English with a positive tone.
- Prefer short sections over long paragraphs.
- Use emojis with restraint to keep the notes engaging, not noisy.
- Link the relevant PRs, docs, and repo references directly.

## Minimal template

```md
## Executive Summary ✨

<1-2 sentences on what changed and why it matters.>

## Highlights 🚀

- Added: <new capability, doc, workflow, or feature>
- Changed: <improvement or refinement to existing behavior>
- Fixed: <bug, ambiguity, or workflow issue removed>
- Removed: <optional; only include when something was intentionally removed>

## Important Details 🧭

- <key implementation or behavior detail users should know>
- <migration, compatibility, or workflow note if relevant>

## New Concepts, Briefly 💡

- `<concept or feature name>`: <1 sentence explanation in plain English>
- `<concept or feature name>`: <1 sentence explanation in plain English>

## References 🔗

- PRs: [#123](https://github.com/<owner>/<repo>/pull/123), [#124](https://github.com/<owner>/<repo>/pull/124)
- Docs: [`AGENTS.md`](../AGENTS.md), [`docs/index.md`](index.md)
- Notes: <link to changelog, issue, or related doc>
```

## Writing tips

- Skip empty sections instead of padding with filler.
- If there is no removal, omit `Removed`.
- Prefer one strong sentence for the executive summary over generic marketing language.
- Explain repo-specific concepts in one sentence as if the reader is new but technical.
- When several PRs land together, group them under one summary instead of repeating the same context.
