# Portfolio. Projects by Safwan

A static portfolio site. It shows a gallery of every project with a category
toggle a visitor can switch between: a 30-day run of daily finance and AI
builds (29 projects), and a set of personal projects. Each project has its own
page; the finance builds add a condensed brief, fun facts and screenshots.

It is a plain, fast website: no server and no AI when someone visits. It is
hosted on GitHub Pages.

Live site: https://x7-u.github.io/day-30-portfolio-site/

## What it shows

- A gallery of all projects with a category toggle (All / Personal Projects /
  30 Day Finance). Each card shows the name, tagline, stack and status.
- A page per project: a condensed brief pulled from the project's overview
  doc (use case, inputs and outputs, how it works, a screenshot walk-through
  and honest limitations), a couple of fun facts, the accounting focus, the
  stack, the build status, the test count, a link to the GitHub repo, and up
  to four screenshots.

## How it is built

The site is generated from the project catalogue by a small build script.
The output is fully static (plain HTML, CSS, the favicon, and the
screenshots).

```
.venv\Scripts\python.exe day-30-portfolio-site\build_site.py
```

That writes a self-contained `docs/` folder. GitHub Pages serves `docs/`
straight from the main branch, so what you push is what goes live.

## Files

```
build_site.py        static site generator (writes docs/)
fun_facts.py         curated per-project fun facts
project_brief.py     condensed brief pulled from each PROJECT_OVERVIEW.docx
portfolio_schema.py  the catalogue: 29 finance builds (CATALOG) + PERSONAL
portfolio_engine.py  scans each folder for build status, tests, screenshots
pipeline.py          ties the scan together
server.py            optional local preview (Flask, port 1030)
templates/           index.html and project.html, shared by builder and preview
static/              style.css, favicon.svg
docs/                the generated static site that GitHub Pages serves
tests/               catalogue, engine, fun-facts and no-dashes checks
```

## Hosting on GitHub Pages

1. Build the site (run `build_site.py`). It writes `docs/`.
2. Commit and push.
3. In the repo Settings, under Pages, set the source to the `main` branch and
   the `/docs` folder. The site is then live at the URL above.

## Local preview (optional)

The same content can be previewed locally with a small Flask app, handy while
editing. The hosted site is the static `docs/` folder, not this server.

```
day-30-portfolio-site\start.bat
```

Opens at `http://127.0.0.1:1030/`.

## Tests

```
pytest day-30-portfolio-site -v
```

Covers the catalogue, the folder scan, the fun facts (every project has at
least two), the project brief extraction, and the no-dashes rule across the
whole tree.
