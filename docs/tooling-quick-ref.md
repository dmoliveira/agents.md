# Tooling Quick Reference

Use this as a fast productivity map for local utility tools.

Detailed references:
- `docs/index.md` for the full docs map
- `docs/codememory-workflow.md` for required Codememory execution flow
- `docs/codememory-conventions.md` for repo-specific Codememory rules
- `docs/github-cli.md` for automation-safe `gh` patterns
- `docs/validation-policy.md` for key-gate validation defaults
- `docs/agent-browser.md` for browser-only blocker handling
- `docs/design-image-decision-guide.md` for design/image generation versus browser-validation routing

## Browser automation decision rule
- Use shell-first automation by default.
- Switch to browser automation only for UI-owned state such as OAuth/install/re-auth/scope acceptance and final visual verification.
- Keep browser scope narrow, then hand control back to shell tooling as soon as the blocker is cleared.
- Treat the browser as a bridge, not the default environment.

## Tool source paths
- Primary external tooling repo: local `utils-scripts` clone when available
- OpenCode config/agent repo: local `my_opencode` clone when available
- If neither exists, continue with repo-native commands and existing project tooling.

## Optional external references
- Use these only when local docs are insufficient; do not preload broad external repo context by default.
- `utils-scripts`
  - local `utils-scripts/docs/workflow-matrix.md` for shortest-path CLI/operator flows
  - local `utils-scripts/TERMINAL_PLAYBOOK.md` for terminal-first work patterns on macOS/Linux
  - local `utils-scripts/docs/cheatsheets/gh.md` for practical GitHub CLI usage
  - local `utils-scripts/docs/cheatsheets/rg.md` for fast search patterns
  - local `utils-scripts/docs/cheatsheets/uv.md` for Python env/test flows
  - local `utils-scripts/docs/cheatsheets/make.md` for repo task runner usage
  - local `utils-scripts/docs/cheatsheets/parallel.md` for safe parallel command patterns
- `my_opencode`
  - local `my_opencode/docs/agents-cheatsheet.md` for agent-selection reminders when you have the runtime repo nearby
  - local `my_opencode/docs/agent-tool-restrictions.md` for maintainer checks on agent boundaries when available
  - local `my_opencode/docs/quickstart.md` for lightweight runtime health commands when available
  - local `my_opencode/docs/image-design-workflow.md` for `/ox-design`, `/image`, provider preference, and output-location preference behavior when available
- Avoid using `utils-scripts/AGENTS.md` as a reference here because its coordination model differs from this repo.

## High-value tools
- `oc` (Codememory): `oc current`, `oc next --scope <repo-scope> --limit 5`, `oc queue --scope <repo-scope> --limit 10`, `oc resume --scope <repo-scope> --task <id>`
- `oc` (capture): `oc add task "title" ...`, `oc add epic "title" ...`, `oc add memory "title" --kind decision|constraint|assumption|convention ...`, `oc add doc "title" ...`
- `oc` (reports/closeout): `oc report improvement "title" --body "..."`, `oc report error "title" --body "..."`, `oc done <task_id> --note "..."`, `oc end-session <session_id> --outcome done|failed|canceled`
- `gh` (task flow): `gh issue list --state open --limit 20`, `gh issue view <id>`, `gh issue comment <id> --body "status update"`, `gh issue close <id>`
- `gh` (PR flow): `gh pr status`, `gh pr view <id>`, `gh pr checks --watch`, `gh api repos/<owner>/<repo>/pulls ...`, `gh pr merge <id> --merge --delete-branch`
- `rg` + `fd` (code search): `fd -e md`, `rg -n "pattern" -g "*.md"`
- `ast-grep` (structural code search): `sg run -p 'console.log($A)' src`, `sg scan -r rules/`
- `tree-sitter-cli` (syntax-aware experiments): `tree-sitter parse path/to/file`, `tree-sitter highlight path/to/file`
- `watchexec` (fast rerun loop): `watchexec -e py,ts -r -- make test`
- `tmux` (persistent panes): keep AI/OpenCode sessions prefixed like `ai-oc-<task>` so cleanup and resume targeting stay obvious
- `uv` (Python): `uv venv .venv`, `uv run pytest -q`, `uv run ruff check .`
- `my_opencode` image workflow when available: `/image access --json`, `/image preference show --json`, `/image location show --json`, `/image generate ...`
- `make` (entrypoint): `make help`, then run project targets instead of ad-hoc scripts.
  - In this repo: `make preflight`, `make wiki-status`, `make wiki-mirror-status`, `make wiki-sync-check`, `make wiki-sync-dry-run`, `make wiki-sync-apply`, `make wiki-fallback-sync-dry-run`, `make wiki-fallback-sync-apply`, `make wiki-fallback-dispatch`, `make wiki-publish-checklist`, `make wiki-probe-dispatch`.

## Remote alignment checks
- Before implementation: run `git fetch --all --prune`, `gh pr status`, and review the selected issue/PR again so the task still matches upstream.
- Before merge: re-check `origin/main`, current PR status, and any overlapping PRs/branches; rebase or update when upstream changed in a way that affects your slice.

## Codememory default flow
- For meaningful work, check Codememory before implementation and use it instead of ad hoc todo lists, including OpenCode's `todowrite`/todo list.
- Start with `oc current`, `oc next`, `oc queue`, and `oc resume --task <id>` when resuming a known slice.
- Create or attach a Codememory task/epic before implementation continues on meaningful requests.
- Prefer a repo-local `.codememory/config.yaml` for the repo scope; otherwise pass `--scope <repo-scope>` explicitly.
- Keep detailed workflow and conventions in the dedicated Codememory docs so the integration can be updated or disabled with minimal churn.

## Parallel execution default
- Prefer `parallel` for independent repeated commands instead of `for` loops.
- Base pattern: `parallel --jobs <n> --halt soon,fail=1 '<cmd {1}>' ::: <arg1> <arg2> <arg3>`
- Use when commands are independent and order does not matter.
- Do not use for ordered/stateful steps, commands with shared mutable state, or cases requiring strict serial logs.
- Fallback when `parallel` is unavailable: `xargs -P <n>`; use sequential execution when steps are dependent.

### Parallel quick recipes
- Run checks in multiple dirs: `parallel --jobs 3 --halt soon,fail=1 'make -C {} test' ::: pkg-a pkg-b pkg-c`
- Run same command on many files: `parallel --jobs 4 --halt soon,fail=1 'ruff check {}' ::: $(fd -e py)`
- Matrix args (paired lists): `parallel --jobs 4 --halt soon,fail=1 'pytest -q {1} --maxfail={2}' ::: tests/a tests/b :::+ 1 2`
- Dry-run first (safe preview): `parallel --dry-run --jobs 4 'ruff check {}' ::: $(fd -e py)`

## Learning loop (if `my_opencode` exists)
- Use mistake ledger reporting to detect repeated failure patterns: `npm run mistake:report -- --mode digest --json`.
- Use `/learn` to capture and publish reusable guidance: `/learn capture --json`, `/learn search --status published --json`.
- For high-risk learn entries, follow approval gates before publish (see `instructions/knowledge_capture_policy_contract.md` in `my_opencode`).
- Example mapping: mistake log (what/impact/fix/prevention) -> `/learn capture --json` draft -> `/learn review ...` -> `/learn publish ...` when confidence and approvals pass.

## Notes
- Keep commands non-interactive and CI-safe.
- Prefer existing repo conventions over generic defaults when they conflict.
- Prefer local CLI/browser/session tools before adding more remote MCP servers when token cost matters.
- Treat `browser-use` and Context7 as opt-in/manual additions: use `browser-use` for higher-level browser-agent work when Playwright is too low-level, and use Context7 only when you have a local CLI path you trust.
