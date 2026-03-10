# AGENTS.md Playbook for Parallel Delivery

This is the repository mirror of the intended GitHub Wiki home page.

Use this page when the wiki git remote (`<repo>.wiki.git`) is not yet provisioned.

- Start here: [README](../README.md)
- Operating contract: [AGENTS.md](../AGENTS.md)
- Docs hub: [docs/index.md](index.md)
- Tooling quick reference: [docs/tooling-quick-ref.md](tooling-quick-ref.md)
- Advanced orchestration: [docs/orchestration-advanced.md](orchestration-advanced.md)
- Support this work: [docs/support-the-project.md](support-the-project.md)

Key behavior:
- Use dedicated worktrees per task.
- Check remote state before coding and again before merge.
- Keep commits small and focused.
- End cycles with `<CONTINUE-LOOP>` when tasks remain or the next execution slice is already clear.
