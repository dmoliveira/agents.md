# Agent Browser Guide

Use this when shell automation reaches a real browser-owned boundary.

## Install and setup
- Keep installation guidance minimal here; browser tooling changes faster than the core agent workflow.
- If your environment already exposes a browser-capable agent or tool, use that first.
- If not, follow the upstream tool's install instructions directly, then come back to this guide for decision rules and workflow shape.
- For `agent-browser`, start from the upstream project: `https://github.com/vercel-labs/agent-browser`.

## Good fit
- OAuth consent screens and third-party login approval
- Shopify app install, re-auth, or scope upgrade prompts in admin
- Final visual verification after the shell-driven change is already in place

## Bad fit
- Repo edits, searches, validation, or routine CLI workflows
- API calls, background jobs, or state you can inspect faster from shell tooling
- Long exploratory browsing without a clear blocker to clear

## Default pattern
- Try shell-first implementation and validation.
- Switch to the browser only for the narrow blocked step.
- Capture the minimum evidence needed.
- Return to shell tooling immediately for the rest of the flow.

## Evidence to capture
- Exact page or prompt reached
- Action taken and why it was needed
- Resulting state change, token grant, install completion, or visible success/failure
- Any follow-up shell command or URL that confirms the browser step worked

## Shopify re-auth example
- Shell flow hits a missing-scope or expired-session boundary.
- Open the Shopify admin re-auth/install prompt.
- Accept the requested scopes or complete the install.
- Return to shell validation and confirm the app can continue the intended API flow.

## GitHub or SaaS OAuth example
- CLI or local app redirects to an OAuth consent screen.
- Approve the exact requested access in the browser.
- Return to the shell or app callback flow and confirm the authenticated operation now succeeds.

## Guardrails
- Keep the browser session scoped to the blocker you are clearing.
- Do not turn browser work into the primary operating environment.
- Prefer reproducible notes over screenshots unless visuals are the point.
- If the browser step expands beyond a narrow unblock, stop and document the new scope explicitly.
