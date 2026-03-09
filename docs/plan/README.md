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
- Use the same status model for full plans and for tracked epics/tasks inside a plan so partial progress stays visible.
- Move a plan to `docs/plan/doing` when execution starts.
- Move it to `docs/plan/blocked` only for a real blocker.
- Move it to `docs/plan/parked` when intentionally paused.
- Move it to `docs/plan/done` after the work lands.
- Move it to `docs/plan/cancelled` when explicitly abandoned or superseded.

## Allowed transitions
- `new` -> `doing`, `cancelled`
- `doing` -> `blocked`, `parked`, `done`, `cancelled`
- `blocked` -> `doing`, `parked`, `cancelled`
- `parked` -> `doing`, `cancelled`
- `done` -> no further moves; create a new plan if follow-up work is needed
- `cancelled` -> no further moves; create a new plan if work is revived

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

For multi-step plans, track child epics/tasks with the same statuses (`new`, `doing`, `blocked`, `parked`, `done`, `cancelled`) in the plan body so it is obvious what finished, paused, or changed direction.
