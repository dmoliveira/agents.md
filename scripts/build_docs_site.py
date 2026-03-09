#!/usr/bin/env python3

from __future__ import annotations

from html import escape
from pathlib import Path
import re


REPO = "dmoliveira/agents.md"
SPONSORS_URL = "https://github.com/sponsors/dmoliveira"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_version(makefile_text: str) -> str:
    match = re.search(r"^PROJECT_VERSION\s*:=\s*(.+)$", makefile_text, re.MULTILINE)
    if not match:
        raise ValueError("PROJECT_VERSION not found in Makefile")
    return match.group(1).strip()


def parse_latest_changelog(changelog_text: str) -> tuple[str, dict[str, list[str]]]:
    lines = changelog_text.splitlines()
    date = ""
    sections: dict[str, list[str]] = {}
    current_section = ""

    for line in lines:
        if line.startswith("## ") and not date:
            date = line[3:].strip()
            continue
        if date and line.startswith("## "):
            break
        if not date:
            continue
        if line.startswith("### "):
            current_section = line[4:].strip()
            sections[current_section] = []
            continue
        if current_section and line.startswith("- "):
            sections[current_section].append(line[2:].strip())

    if not date:
        raise ValueError("Latest changelog entry not found")
    return date, sections


def path_to_github_url(path_text: str) -> str:
    normalized = path_text.strip()
    if normalized == "../AGENTS.md":
        normalized = "AGENTS.md"
    elif normalized.startswith("../"):
        normalized = normalized[3:]
    else:
        normalized = f"docs/{normalized}"
    return f"https://github.com/{REPO}/blob/main/{normalized}"


def parse_docs_index(index_text: str) -> list[tuple[str, list[tuple[str, str]]]]:
    sections: list[tuple[str, list[tuple[str, str]]]] = []
    current_title = ""
    current_items: list[tuple[str, str]] = []
    pattern = re.compile(r"^- `([^`]+)`: (.+)$")

    for line in index_text.splitlines():
        if line.startswith("## "):
            if current_title:
                sections.append((current_title, current_items))
            current_title = line[3:].strip()
            current_items = []
            continue
        match = pattern.match(line)
        if match:
            current_items.append((match.group(1), match.group(2)))

    if current_title:
        sections.append((current_title, current_items))
    return sections


def render_release_lists(sections: dict[str, list[str]], max_items: int = 6) -> str:
    blocks: list[str] = []
    for name, items in sections.items():
        if not items:
            continue
        visible = items[:max_items]
        items_html = "".join(f"<li>{escape(item)}</li>" for item in visible)
        if len(items) > max_items:
            remaining = len(items) - max_items
            items_html += f"<li><em>+{remaining} more notes in the full changelog and release page.</em></li>"
        blocks.append(
            '<section class="release-block">'
            f"<h3>{escape(name)}</h3>"
            f"<ul>{items_html}</ul>"
            "</section>"
        )
    return "".join(blocks)


def render_docs_sections(sections: list[tuple[str, list[tuple[str, str]]]]) -> str:
    html_parts: list[str] = []
    for title, items in sections:
        links = []
        for path_text, description in items:
            href = path_to_github_url(path_text)
            links.append(
                "<li>"
                f'<a href="{href}">{escape(path_text)}</a>'
                f"<span>{escape(description)}</span>"
                "</li>"
            )
        html_parts.append(
            '<section class="map-card">'
            f"<h3>{escape(title)}</h3>"
            f"<ul>{''.join(links)}</ul>"
            "</section>"
        )
    return "".join(html_parts)


def build_html(
    version: str,
    changelog_date: str,
    release_sections: dict[str, list[str]],
    docs_sections: list[tuple[str, list[tuple[str, str]]]],
) -> str:
    release_url = f"https://github.com/{REPO}/releases/tag/v{version}"
    repo_url = f"https://github.com/{REPO}"
    pages_url = f"https://{REPO.split('/')[0]}.github.io/{REPO.split('/')[1]}/"
    release_html = render_release_lists(release_sections)
    docs_html = render_docs_sections(docs_sections)
    quick_steps = "".join(
        [
            "<li><strong>Read</strong><span>Start with AGENTS.md and the docs hub.</span></li>",
            "<li><strong>Branch</strong><span>Create a dedicated worktree for one scoped task.</span></li>",
            "<li><strong>Ship</strong><span>Iterate fast, validate at the pre-PR gate, then commit once.</span></li>",
        ]
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AGENTS.md Playbook</title>
    <style>
      :root {{
        color-scheme: light;
        --bg: #f5efe4;
        --panel: rgba(255, 251, 246, 0.9);
        --card: #fffdf9;
        --text: #211914;
        --muted: #6a5a4f;
        --accent: #9c4b1d;
        --accent-2: #0d7869;
        --accent-3: #153d66;
        --border: #eadbc9;
        --shadow: 0 18px 52px rgba(49, 29, 16, 0.12);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
        color: var(--text);
        background:
          radial-gradient(circle at top left, rgba(255, 216, 176, 0.65), transparent 28%),
          radial-gradient(circle at bottom right, rgba(171, 227, 214, 0.55), transparent 24%),
          linear-gradient(180deg, #fbf6ee, #f2ece2 58%, #efe7db);
      }}
      a {{ color: var(--accent); text-decoration: none; }}
      a:hover {{ text-decoration: underline; }}
      .wrap {{ max-width: 1180px; margin: 0 auto; padding: 24px 20px 64px; }}
      .topbar {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
      }}
      .brand {{ font-size: 0.95rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); }}
      .nav {{ display: flex; flex-wrap: wrap; gap: 10px; }}
      .nav a {{
        padding: 9px 12px;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(255,255,255,0.55);
        color: var(--text);
        font-size: 0.92rem;
      }}
      .hero {{
        display: grid;
        gap: 24px;
        grid-template-columns: 1.4fr 0.95fr;
        align-items: stretch;
        margin-bottom: 28px;
      }}
      .hero-card, .panel {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(8px);
      }}
      .hero-card {{ padding: 32px; position: relative; overflow: hidden; }}
      .hero-card::after {{
        content: "";
        position: absolute;
        inset: auto -40px -60px auto;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(164, 74, 25, 0.18), transparent 68%);
      }}
      .eyebrow {{
        display: inline-flex;
        gap: 10px;
        align-items: center;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.72);
        color: var(--accent);
        font-size: 0.86rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }}
      h1 {{ font-size: clamp(2.5rem, 5vw, 4.4rem); line-height: 0.96; margin: 18px 0 14px; }}
      .hero p {{ font-size: 1.07rem; line-height: 1.65; color: var(--muted); margin: 0 0 18px; }}
      .hero-meta {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}
      .meta-chip {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.72);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 8px 12px;
        color: var(--text);
        font-size: 0.92rem;
      }}
      .cta-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }}
      .btn {{
        display: inline-flex; align-items: center; justify-content: center;
        padding: 12px 18px; border-radius: 999px; font-weight: 700; border: 1px solid transparent;
      }}
      .btn-primary {{ background: var(--accent); color: #fffaf6; }}
      .btn-secondary {{ background: transparent; border-color: var(--border); color: var(--text); }}
      .stats {{ padding: 26px; display: grid; gap: 14px; }}
      .stat {{ padding: 14px 0; border-bottom: 1px solid var(--border); }}
      .stat:last-child {{ border-bottom: 0; }}
      .stat-label {{ display: block; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); margin-bottom: 6px; }}
      .stat-value {{ font-size: 1.45rem; font-weight: 700; }}
      .mini-note {{ color: var(--muted); font-size: 0.95rem; margin: 0; }}
      .step-list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }}
      .step-list li {{
        display: grid;
        grid-template-columns: 88px 1fr;
        gap: 14px;
        align-items: start;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 14px 16px;
      }}
      .step-list strong {{ color: var(--accent-3); text-transform: uppercase; font-size: 0.86rem; letter-spacing: 0.04em; }}
      .step-list span {{ color: var(--muted); line-height: 1.5; }}
      .grid {{ display: grid; grid-template-columns: 1.08fr 0.92fr; gap: 24px; margin-bottom: 24px; }}
      .panel {{ padding: 28px; }}
      h2 {{ margin: 0 0 14px; font-size: 1.55rem; }}
      .release-grid {{ display: grid; gap: 16px; }}
      .release-block {{ background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 18px 18px 6px; }}
      .release-block h3 {{ margin: 0 0 8px; font-size: 1.05rem; color: var(--accent-2); }}
      .release-block ul, .map-card ul {{ margin: 0; padding-left: 20px; }}
      .release-block li, .map-card li {{ margin: 0 0 10px; line-height: 1.5; }}
      .map {{ display: grid; gap: 16px; }}
      .map-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 18px; }}
      .map-card h3 {{ margin: 0 0 10px; font-size: 1.02rem; }}
      .map-card li span {{ display: block; color: var(--muted); margin-top: 3px; }}
      .map-card li a {{ font-weight: 700; }}
      .donation {{
        display: grid; grid-template-columns: 1.2fr auto; gap: 20px; align-items: center;
        background: linear-gradient(135deg, rgba(164, 74, 25, 0.92), rgba(82, 36, 16, 0.95));
        color: #fff8f0;
        border-radius: 24px;
        padding: 28px;
        box-shadow: var(--shadow);
      }}
      .donation h2, .donation p {{ color: inherit; margin: 0 0 10px; }}
      .donation .btn-primary {{ background: #fff3e3; color: #7d3310; }}
      .donation .btn-secondary {{ border-color: rgba(255,255,255,0.3); color: #fff8f0; }}
      .footnote {{ margin-top: 18px; color: var(--muted); font-size: 0.94rem; }}
      @media (max-width: 860px) {{
        .hero, .grid, .donation {{ grid-template-columns: 1fr; }}
        .topbar {{ align-items: flex-start; }}
        .wrap {{ padding: 24px 16px 48px; }}
        .hero-card, .panel, .donation {{ padding: 22px; }}
        .step-list li {{ grid-template-columns: 1fr; gap: 8px; }}
      }}
    </style>
  </head>
  <body>
    <main class="wrap">
      <header class="topbar">
        <div class="brand">AGENTS.md Playbook</div>
        <nav class="nav">
          <a href="https://github.com/{REPO}/blob/main/docs/index.md">Docs Hub</a>
          <a href="https://github.com/{REPO}/blob/main/AGENTS.md">Contract</a>
          <a href="{release_url}">Release Notes</a>
          <a href="{SPONSORS_URL}">Sponsor</a>
        </nav>
      </header>
      <section class="hero">
        <article class="hero-card">
          <span class="eyebrow">Fresh on GitHub Pages</span>
          <h1>Parallel agent delivery, without the coordination drift.</h1>
          <p>
            A production-minded playbook for worktree-based execution, key-gate validation,
            focused commits, and clean handoffs. This landing page is generated from the repo's
            docs index, changelog, and release metadata so it stays current with the latest notes.
          </p>
          <div class="hero-meta">
            <span class="meta-chip">Release v{escape(version)}</span>
            <span class="meta-chip">Updated from {escape(changelog_date)}</span>
            <span class="meta-chip">Native tools only</span>
          </div>
          <div class="cta-row">
            <a class="btn btn-primary" href="{repo_url}">Open the repository</a>
            <a class="btn btn-secondary" href="https://github.com/{REPO}/blob/main/docs/index.md">Browse the docs hub</a>
            <a class="btn btn-secondary" href="https://github.com/{REPO}/blob/main/AGENTS.md">Read AGENTS.md</a>
          </div>
        </article>
        <aside class="hero-card stats">
          <div class="stat">
            <span class="stat-label">GitHub Pages</span>
            <span class="stat-value"><a href="{pages_url}">Live docs site</a></span>
          </div>
          <div class="stat">
            <span class="stat-label">Latest release</span>
            <span class="stat-value"><a href="{release_url}">v{escape(version)}</a></span>
          </div>
          <div class="stat">
            <span class="stat-label">Release notes date</span>
            <span class="stat-value">{escape(changelog_date)}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Delivery style</span>
            <span class="stat-value">Worktrees + key-gate validation</span>
          </div>
          <p class="mini-note">Pages, docs, and release notes stay aligned through `make site-build` during preflight and deploy.</p>
        </aside>
      </section>

      <section class="grid">
        <article class="panel">
          <h2>Quick start</h2>
          <p>Use the page as a launchpad: understand the model, jump into the contract, then ship from a dedicated worktree.</p>
          <ol class="step-list">{quick_steps}</ol>
        </article>
        <aside class="panel">
          <h2>What this optimizes for</h2>
          <p class="mini-note">A tighter delivery loop with less review churn, fewer coordination mistakes, and faster onboarding for both people and agents.</p>
          <ol class="step-list">
            <li><strong>Scope</strong><span>One issue or task at a time to reduce branch and context drift.</span></li>
            <li><strong>Speed</strong><span>Fast local iteration, then required validation at key gates instead of every edit.</span></li>
            <li><strong>Clarity</strong><span>Concise docs, a docs hub, and explicit plan states so active work is obvious.</span></li>
          </ol>
        </aside>
      </section>

      <section class="grid">
        <article class="panel">
          <h2>Latest release notes</h2>
          <p>
            Generated from `CHANGELOG.md` and linked to the latest tagged release so readers can
            see what changed without hunting through commits.
          </p>
          <div class="release-grid">{release_html}</div>
          <p><a href="{release_url}">Open the full release notes on GitHub</a></p>
        </article>
        <aside class="panel">
          <h2>Docs map</h2>
          <p>Generated from `docs/index.md` so the page reflects the current operator entrypoints.</p>
          <div class="map">{docs_html}</div>
        </aside>
      </section>

      <section class="donation">
        <div>
          <h2>Back the next playbook upgrade</h2>
          <p>
            If this repo helps your team ship faster with less agent chaos, support the maintenance
            work that keeps the docs, examples, and safer defaults improving release after release.
          </p>
          <p>Every sponsor helps fund tighter guidance, cleaner automation, and more practical examples.</p>
        </div>
        <div class="cta-row">
          <a class="btn btn-primary" href="{SPONSORS_URL}">Sponsor the work</a>
          <a class="btn btn-secondary" href="https://github.com/{REPO}/blob/main/docs/support-the-project.md">More ways to help</a>
        </div>
      </section>

      <p class="footnote">
        Generated from repo notes in `CHANGELOG.md`, `Makefile`, and `docs/index.md`.
      </p>
    </main>
  </body>
</html>
"""


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    version = parse_version(read_text(repo_root / "Makefile"))
    changelog_date, release_sections = parse_latest_changelog(
        read_text(repo_root / "CHANGELOG.md")
    )
    docs_sections = parse_docs_index(read_text(repo_root / "docs" / "index.md"))
    html = build_html(version, changelog_date, release_sections, docs_sections)
    output = repo_root / "docs" / "site" / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"site-build: wrote {output.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
