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
- deliver small commits and PRs,
- validate before merge,
- and keep communication systematic with explicit end-of-cycle signals like `<CONTINUE-LOOP>`.

## Why this exists 🧭

Most teams do not fail from lack of AI capability; they fail from coordination drift.

This playbook focuses on practical controls for multi-agent execution:
- predictable task ownership with `br` issue IDs,
- e2e worktree flow (`wt flow`) for safe branch isolation,
- risk-based review/fix/improve passes,
- concise final-response patterns that make pending work obvious.

## Start in 5 minutes ⏱️

1. Read `AGENTS.md`.
2. Initialize tracking with `br init`.
3. Pick an item with `br ready`.
4. Move it to active: `br update <id> --status in_progress`.
5. Execute delivery work in a dedicated worktree branch (never directly on `main`).

For full command detail, use:
- `docs/tooling-quick-ref.md`
- `docs/orchestration-advanced.md`

## What is in this repo 📚

- `AGENTS.md`: source-of-truth operating contract.
- `docs/tooling-quick-ref.md`: quick commands for `br`, `gh`, search, `uv`, and parallel execution.
- `docs/orchestration-advanced.md`: high-pressure and high-risk orchestration controls.
- `docs/support-the-project.md`: donation and sustainability options.
- `docs/wiki-home-snippet.md`: copy/paste block for the GitHub Wiki home page.

## Workflow highlights (wt flow e2e) 🔁

- create a dedicated worktree and branch for each feature/bug/task,
- implement with small, logical commits,
- run review/fix/improve passes according to risk,
- open PR, validate checks, merge,
- cleanup worktree, sync `main`, close the `br` issue.

Reference flow:

```bash
git checkout main
git pull --rebase
git worktree add ../<branch> -b <branch>
# implement + small commits
git push -u origin <branch>
gh pr create
# after merge
git worktree remove ../<branch>
git pull --rebase
```

## Magic continue keyword ✨

When requested scope still has pending tasks, the final line should be:

`<CONTINUE-LOOP>`

This keeps execution cycles explicit and prevents accidental early handoff.

## External tools used 🔧

- `br` (beads_rust): issue tracking for agent workflows.
- `gh`: GitHub CLI for PR lifecycle and checks.
- `uv`: Python environment and package tooling.
- `ruff`: Python lint/format.
- `rg` and `fd`: fast search and discovery.
- GNU `parallel`: parallelized independent command execution.

Useful links:
- Beads (`br`): https://github.com/automazeio/beads
- GitHub CLI (`gh`): https://cli.github.com/
- uv: https://docs.astral.sh/uv/
- Ruff: https://docs.astral.sh/ruff/
- ripgrep (`rg`): https://github.com/BurntSushi/ripgrep
- fd: https://github.com/sharkdp/fd
- GNU parallel: https://www.gnu.org/software/parallel/

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
