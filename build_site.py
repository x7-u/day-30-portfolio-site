"""Day 30. Static site builder for GitHub Pages.

Renders the portfolio to a self-contained ``docs/`` folder of plain HTML, so
it can be served as a static website (no Flask, no Python, no AI at view
time). GitHub Pages can serve ``docs/`` straight from the main branch.

What it does:
  1. Scans the project folders for the catalogue (the same engine the local
     server uses).
  2. Renders the home page and one page per project with Jinja2.
  3. Rewrites the app's absolute URLs to relative ones so the site works from
     any base path (for example https://<user>.github.io/<repo>/).
  4. Copies the stylesheet, the favicon, and each project's screenshots into
     ``docs/assets/``.
  5. Drops a ``.nojekyll`` marker so GitHub Pages serves the files as-is.

Run it with the project's Python:
    .venv\\Scripts\\python.exe day-30-portfolio-site\\build_site.py
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from fun_facts import fun_facts_for
from jinja2 import Environment, FileSystemLoader, select_autoescape
from portfolio_engine import all_summaries, home_context
from project_brief import brief_for

OUT = HERE / "docs"
ASSETS = OUT / "assets"
STATIC = HERE / "static"
TEMPLATES = HERE / "templates"
ASSET_FILES = ("style.css", "favicon.svg")
MAX_SHOTS = 4   # screenshots shown per project, to keep the site light and fast

# Hard rule for this project: no em-dashes or en-dashes anywhere in output.
_DASH = str.maketrans({"\u2014": "-", "\u2013": "-"})


def to_relative(html: str) -> str:
    """Rewrite the app's absolute URLs to page-relative URLs and strip any
    stray em/en dashes, so the page is portable and dash-free."""
    html = html.replace('href="/static/', 'href="assets/')
    html = html.replace('src="/static/', 'src="assets/')
    html = re.sub(r'href="/project/([a-z0-9\-]+)"', r'href="\1.html"', html)
    html = re.sub(r'src="/shots/([a-z0-9\-]+)/([^"]+)"', r'src="assets/shots/\1/\2"', html)
    html = re.sub(r'href="/shots/([a-z0-9\-]+)/([^"]+)"', r'href="assets/shots/\1/\2"', html)
    html = html.replace('href="/"', 'href="index.html"')
    return html.translate(_DASH)


def _copy_assets(summaries) -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name in ASSET_FILES:
        src = STATIC / name
        if src.is_file():
            shutil.copy(src, ASSETS / name)
    shot_count = 0
    for s in summaries:
        folder = s.project.folder
        src_shots = PROJECT_ROOT / folder / "shots"
        if not src_shots.is_dir():
            continue
        dst = ASSETS / "shots" / folder
        dst.mkdir(parents=True, exist_ok=True)
        for png in sorted(src_shots.glob("*.png"))[:MAX_SHOTS]:
            shutil.copy(png, dst / png.name)
            shot_count += 1
    return shot_count


def build() -> dict:
    summaries = all_summaries(PROJECT_ROOT)
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
    )

    # Fresh output folder.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # Home page.
    index_html = env.get_template("index.html").render(portfolio=home_context(summaries))
    (OUT / "index.html").write_text(to_relative(index_html), encoding="utf-8")

    # One page per project.
    project_tmpl = env.get_template("project.html")
    pages = 0
    for s in summaries:
        proj = s.to_dict()
        proj["shots"] = (proj.get("shots") or [])[:MAX_SHOTS]
        proj["brief"] = brief_for(PROJECT_ROOT / s.project.folder)
        if s.project.category == "personal":
            proj["fun_facts"] = []
        else:
            proj["fun_facts"] = fun_facts_for(s)
        html = project_tmpl.render(project=proj)
        (OUT / f"{s.project.folder}.html").write_text(to_relative(html), encoding="utf-8")
        pages += 1

    shot_count = _copy_assets(summaries)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    return {
        "pages": pages + 1,
        "projects": len(summaries),
        "screenshots": shot_count,
        "out": str(OUT),
    }


if __name__ == "__main__":
    stats = build()
    print(
        f"Built {stats['pages']} pages "
        f"({stats['projects']} projects, {stats['screenshots']} screenshots) "
        f"into {stats['out']}"
    )
