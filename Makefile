PROJECT_NAME := agents.md
PROJECT_VERSION := 0.1.0
REPO ?= dmoliveira/agents.md

.PHONY: help preflight docs-checks-dispatch pages-dispatch wiki-status wiki-mirror-status

help:
	@printf "%s v%s\n" "$(PROJECT_NAME)" "$(PROJECT_VERSION)"
	@printf "Available targets:\n"
	@printf "  %-24s %s\n" "help" "Show this help"
	@printf "  %-24s %s\n" "preflight" "Validate auth, workflows, and wiki readiness"
	@printf "  %-24s %s\n" "docs-checks-dispatch" "Trigger docs link checks workflow"
	@printf "  %-24s %s\n" "pages-dispatch" "Trigger docs Pages deploy workflow"
	@printf "  %-24s %s\n" "wiki-status" "Check wiki/pages status and wiki git provisioning"
	@printf "  %-24s %s\n" "wiki-mirror-status" "Check fallback wiki mirror docs presence"

preflight:
	gh auth status >/dev/null
	gh workflow view docs-links.yml --repo "$(REPO)" >/dev/null
	gh workflow view pages.yml --repo "$(REPO)" >/dev/null
	$(MAKE) wiki-status
	$(MAKE) wiki-mirror-status
	@printf "preflight: ok\n"

docs-checks-dispatch:
	gh workflow run docs-links.yml --repo "$(REPO)"

pages-dispatch:
	gh workflow run pages.yml --repo "$(REPO)"

wiki-status:
	gh api repos/$(REPO) --jq '{has_wiki: .has_wiki, has_pages: .has_pages, default_branch: .default_branch}'
	@if git ls-remote "https://github.com/$(REPO).wiki.git" HEAD >/dev/null 2>&1; then \
		printf "wiki git remote: ready\n"; \
	else \
		printf "wiki git remote: not ready (create first wiki page in UI, then retry)\n"; \
	fi

wiki-mirror-status:
	@if [ -f docs/wiki-home-mirror.md ]; then \
		printf "wiki mirror: docs/wiki-home-mirror.md present\n"; \
	else \
		printf "wiki mirror: missing docs/wiki-home-mirror.md\n"; \
		exit 1; \
	fi
