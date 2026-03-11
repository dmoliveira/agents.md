# AGENTS.md Playbook for Parallel Delivery 🤝

[![Last Commit](https://img.shields.io/github/last-commit/dmoliveira/agents.md)](https://github.com/dmoliveira/agents.md/commits/main)
[![Open Issues](https://img.shields.io/github/issues/dmoliveira/agents.md)](https://github.com/dmoliveira/agents.md/issues)
[![Stars](https://img.shields.io/github/stars/dmoliveira/agents.md?style=social)](https://github.com/dmoliveira/agents.md/stargazers)
[![Docs Quality Checks](https://github.com/dmoliveira/agents.md/actions/workflows/docs-links.yml/badge.svg)](https://github.com/dmoliveira/agents.md/actions/workflows/docs-links.yml)
[![Docs Site Deploy](https://github.com/dmoliveira/agents.md/actions/workflows/pages.yml/badge.svg)](https://github.com/dmoliveira/agents.md/actions/workflows/pages.yml)
[![Docs](https://img.shields.io/badge/docs-in_repo-0a7ea4)](docs/)
[![Wiki](https://img.shields.io/badge/wiki-github-1f6feb)](https://github.com/dmoliveira/agents.md/wiki)
[![GitHub Pages](https://img.shields.io/badge/site-github_pages-2ea44f)](https://dmoliveira.github.io/agents.md/)
[![Model: GPT-5.3 Codex](https://img.shields.io/badge/model-gpt--5.3--codex-8a2be2)](https://platform.openai.com/docs/models)
[![Visuals: GPT-Image-1.5](https://img.shields.io/badge/visuals-gpt--image--1.5-ff7f50)](https://platform.openai.com/docs/guides/image-generation)
[![Support](https://img.shields.io/badge/support-future_projects-ffb300?logo=githubsponsors&logoColor=white)](docs/support-the-project.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Practical guidance for running AI agents in parallel with a consistent, auditable, and non-chaotic workflow.

This repository centers on a production-style `AGENTS.md` contract so agents can:
- pick one issue at a time,
- execute in dedicated worktrees,
- deliver focused commits and PRs,
- validate before merge,
- and keep communication systematic with explicit end-of-cycle signals like `<CONTINUE-LOOP>`.

## Why this exists 🧭

Most teams do not fail from lack of AI capability; they fail from coordination drift.

This playbook focuses on practical controls for multi-agent execution:
- predictable task ownership with native issue IDs,
- e2e worktree flow (`wt flow`) for safe branch isolation,
- remote alignment checks before implementation and again right before merge,
- autonomous execution that keeps moving while a safe next step is clear,
- key-gate validation (pre-PR required, pre-merge conditional),
- concise final-response patterns that make pending work obvious.

## Start in 5 minutes ⏱️

1. Read `AGENTS.md`.
   - If resuming a previous session, re-read `AGENTS.md` and the workflow docs you will use so repo changes beat stale session memory.
2. Sync/check remote state so local context matches the latest branch and PR status.
3. List and pick a scoped item with `gh issue list --state open --limit 20`.
4. Review context with `gh issue view <id>` and confirm it still fits upstream.
5. Mark it active using labels/status/projects in GitHub.
6. Execute delivery work in a dedicated worktree branch (never directly on `main`).

For full command detail, use:
- `docs/index.md`
- `docs/tooling-quick-ref.md`
- `docs/github-cli.md`
- `docs/validation-policy.md`
- `docs/orchestration-advanced.md`
- `make help` for operator shortcuts
- `make preflight` before long execution loops

## What is in this repo 📚

- `AGENTS.md`: source-of-truth operating contract.
- `docs/index.md`: concise hub for core workflow, planning, and wiki docs.
- `docs/tooling-quick-ref.md`, `docs/github-cli.md`, `docs/validation-policy.md`, `docs/orchestration-advanced.md`: daily operator references.
- `docs/plan/README.md`: status model for AI planning docs under `docs/plan/`.
- `docs/site/index.html`: generated GitHub Pages landing page with latest release notes from repo docs.
- `docs/wiki-*`: wiki provisioning, mirror, and fallback publication docs.
- `Makefile`: non-interactive operator shortcuts for docs workflows and checks.

For ongoing readiness checks, run `make wiki-probe-dispatch` to trigger the scheduled wiki probe workflow on demand.
For publishable fallback sync, use `make wiki-fallback-sync-dry-run` and `make wiki-fallback-sync-apply`.
For automated fallback sync in CI, configure `FALLBACK_REPO_TOKEN` and run `make wiki-fallback-dispatch`.

## Workflow highlights (wt flow e2e) 🔁

- create a dedicated worktree and branch for each feature/bug/task,
- check remote branch and PR state before implementing so overlapping AI work is caught early,
- iterate quickly, then commit once per validated slice,
- run review/fix/improve passes according to risk,
- do one final upstream/overlap check before merge to avoid stale or conflicting changes,
- open PR, validate checks, merge,
- cleanup worktree, sync `main`, close the corresponding issue.

Reference flow:

```bash
git checkout main
git pull --rebase
git worktree add ../<branch> -b <branch>
# confirm issue/PR scope still matches latest upstream before coding
# implement + validate, then one focused commit
git push -u origin <branch>
# create PR (prefer `gh api`; see docs/github-cli.md)
# re-check origin/main and overlapping PRs before merge
# after merge
git worktree remove ../<branch>
git pull --rebase
```

## Magic continue keyword ✨

When requested scope still has pending tasks, the final line should be:

`<CONTINUE-LOOP>`

Use the same keyword when the next plan slice is already clear and execution should continue without an early handoff.
Do not present remaining in-scope work as generic "next steps" when the agent can keep going; use `<CONTINUE-LOOP>` instead.
For visible progress notes, command summaries, and local test reporting, use one local timestamp prefix per related block so execution history is easier to trace without adding noise to every line.

## External tools used 🔧

- native GitHub issue tracking via `gh` and repository workflows.
- `gh`: GitHub CLI for PR lifecycle and checks.
- `uv`: Python environment and package tooling.
- `ruff`: Python lint/format.
- `rg` and `fd`: fast search and discovery.
- GNU `parallel`: parallelized independent command execution.

The GitHub Pages site is generated from repo notes with `make site-build` and deployed by `.github/workflows/pages.yml`.

Useful links:
- GitHub CLI (`gh`): https://cli.github.com/
- uv: https://docs.astral.sh/uv/
- Ruff: https://docs.astral.sh/ruff/
- ripgrep (`rg`): https://github.com/BurntSushi/ripgrep
- fd: https://github.com/sharkdp/fd
- GNU parallel: https://www.gnu.org/software/parallel/

Native issue and PR command usage is documented in `AGENTS.md`, `docs/index.md`, `docs/tooling-quick-ref.md`, and `docs/github-cli.md`.

## Docs, Wiki, and GitHub Pages 🌐

- Docs folder: `docs/`
- Wiki home: https://github.com/dmoliveira/agents.md/wiki
- GitHub Pages site: https://dmoliveira.github.io/agents.md/

If you maintain this repo, keep README, docs, wiki, and pages aligned so new contributors can onboard quickly.

## Support this project 💛

If this helps your team ship faster and safer, consider supporting maintenance and future open projects:
- Donation options: `docs/support-the-project.md`
- GitHub Sponsors: https://github.com/sponsors/dmoliveira

Every contribution (code, docs, sponsorship, issue triage) keeps the playbook useful and current.
