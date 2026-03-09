# Plan Statuses

Keep AI planning docs in status folders so active, paused, and historical work stay easy to distinguish.

## Status folders
- `new`: drafted plans not yet started
- `doing`: active plans tied to current execution
- `blocked`: started plans waiting on a concrete blocker
- `parked`: intentionally paused plans that are not active now
- `done`: completed plans kept for reference
- `cancelled`: dropped or superseded plans that should not be resumed

## Agent rules
- Create new plans in `docs/plan/new`.
- Move a plan to `docs/plan/doing` when execution starts.
- Move it to `docs/plan/blocked` only for a real blocker.
- Move it to `docs/plan/parked` when intentionally paused.
- Move it to `docs/plan/done` after the work lands.
- Move it to `docs/plan/cancelled` when explicitly abandoned or superseded.

## Recommended frontmatter
```md
---
status: doing
priority: high
issue: 123
pr: 56
updated: 2026-03-09
---
```
