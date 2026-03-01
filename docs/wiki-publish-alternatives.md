# Wiki Publish Alternatives

Use this guide when GitHub Wiki git remote provisioning is blocked and you still need reliable publication paths.

## Preferred path (when available)

1. Publish/update GitHub Wiki Home page.
2. Keep `docs/wiki-home-snippet.md` and `docs/wiki-home-mirror.md` consistent.
3. Validate with `make wiki-sync-check`.

## Alternative path A: In-repo mirror (recommended fallback)

- Treat `docs/wiki-home-mirror.md` as the live source while `.wiki.git` is unavailable.
- Link stakeholders to the mirror file from PR descriptions and release notes.
- Keep updates small and validated via `make preflight`.

## Alternative path B: GitHub Pages docs

- Publish updates through repository docs and GitHub Pages.
- Route readers to:
  - `docs/wiki-home-mirror.md`
  - `docs/wiki-bootstrap-runbook.md`
  - `docs/operations-loop-runbook.md`

## Operator checklist

Before each publish cycle:

```bash
make preflight
make wiki-sync-check
```

If wiki is still not provisioned, proceed with the in-repo mirror path.
