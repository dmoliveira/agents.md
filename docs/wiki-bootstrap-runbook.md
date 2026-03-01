# Wiki Bootstrap Runbook

Use this runbook when wiki automation is blocked with:

`Repository not found` for `https://github.com/<owner>/<repo>.wiki.git`.

## Why it happens

Some repositories do not provision the wiki git remote until the first wiki page exists.

## Manual bootstrap (one-time)

1. Open the repository wiki in GitHub UI.
2. Create the first page (recommended title: `Home`).
3. Paste content from `docs/wiki-home-snippet.md`.
4. Save the page.

## Verify provisioning

Run:

```bash
git clone https://github.com/<owner>/<repo>.wiki.git
```

If clone succeeds, the wiki git remote is provisioned and automation can continue.

## After provisioning

- Keep wiki updates in sync with `README.md` and `docs/` changes.
- Use small commits with clear PR notes.
- End ongoing delivery loops with `<CONTINUE-LOOP>` only when requested tasks still remain.
