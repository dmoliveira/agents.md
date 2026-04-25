# Design image decision guide

Use this guide when a task touches UX visuals, design artifacts, or image generation.

## Use image/design generation when

- you are exploring concepts before implementation
- you need icons, palettes, wireframes, mockups, hero drafts, or typography directions
- a screenshot or product brief needs stronger visual directions
- the question is **what could this look like?**

## Use browser review when

- the UI already exists and needs verification
- you need responsive, accessibility, loading, empty, or error-state checks
- the task crosses a browser-owned boundary such as OAuth, install, re-auth, or scope acceptance
- the question is **how does the real thing behave?**

## Recommended split

- if you are using the `my_opencode` OpenCode runtime: concept and asset planning -> `/ox-design`
- if you are using the `my_opencode` OpenCode runtime: explicit OpenAI-backed artifact generation -> `/image`
- if you are using the `my_opencode` OpenCode runtime: real implemented UX review -> `/ox-ux`
- otherwise: use your repo-local design workflow for concepting/assets and keep browser usage scoped to implemented-UI validation or narrow browser-owned blockers

## Artifact posture

When design outputs matter to delivery, keep them repo-native under:

```text
artifacts/design/
```

Commit curated assets when they materially help implementation, review, or communication.
