# GitHub CLI Patterns

Use this file for automation-safe GitHub command patterns in this repo.

## Default split
- Use `gh pr` and `gh issue` for read/status flows.
- Prefer `gh api` for automation-critical write operations when deterministic behavior matters.

## Read and status
```bash
gh issue list --state open --limit 20
gh issue view <id>
gh pr status
gh pr view <id>
gh pr checks <id>
```

## Preferred PR creation
Use `gh api` when local guards or wrappers can block `gh pr create`.

```bash
gh api repos/<owner>/<repo>/pulls \
  -f title='docs: title' \
  -f head='<branch>' \
  -f base='main' \
  -f body='## Summary\n- ...\n\n## Validation\n- test: ...\n- lint: ...'
```

## Common write operations
```bash
gh issue comment <id> --body "status update"
gh issue close <id>

gh api repos/<owner>/<repo>/issues/<id>/comments -f body='status update'
gh api repos/<owner>/<repo>/issues/<id>/labels -f labels='docs,ready'
```

## Notes
- Keep commands non-interactive and CI-safe.
- Prefer `gh api` for PR comments, labels, and metadata updates in headless runs.
- If `gh pr create` works cleanly, it is still fine for local/manual usage.
