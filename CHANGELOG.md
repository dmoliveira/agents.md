# Changelog

All notable changes to this project are documented in this file.

## 2026-03-01

### Added
- Practical root `README.md` explaining parallel agent workflow, `wt flow e2e`, and the `<CONTINUE-LOOP>` continuation signal.
- Support documentation at `docs/support-the-project.md` and a reusable Wiki block at `docs/wiki-home-snippet.md`.
- MIT license at `LICENSE`.
- GitHub Pages deployment workflow at `.github/workflows/pages.yml`.
- Docs quality workflow at `.github/workflows/docs-links.yml`.
- Static docs landing page at `docs/site/index.html`.

### Changed
- `README.md` badges now include a Docs Site Deploy workflow badge.
- `README.md` badges now include a Docs Quality Checks workflow badge.
- `docs/wiki-home-snippet.md` now includes a wiki bootstrap note for `Repository not found` cases.
- `README.md` tool links now keep `br` guidance internal to avoid stale external references.
- Added `docs/wiki-bootstrap-runbook.md` for first-time wiki provisioning and enabled manual dispatch for docs link checks.
