# Portfolio. 30 days of finance + AI

A static portfolio site for a 30-day run of daily finance and AI builds. It
shows a filterable gallery of all 29 prior projects, and a page per project
with a couple of plain-English fun facts and a few screenshots.

It is a plain, fast website: no server and no AI when someone visits. It is
hosted on GitHub Pages.

Live site: https://x7-u.github.io/day-30-portfolio-site/

## What it shows

- A gallery: one card per project with the day number, name, tagline, tags,
  stack, build status and test count. Filter the gallery by tag.
- A page per project: a couple of fun facts about what the build does, the
  accounting focus, the technology used, the build status, the test count,
  and up to four screenshots.

## How it is built

The site is generated from the project catalogue by a small build script.
The output is fully static (plain HTML, CSS, one tiny script for the tag
filter, the favicon, and the screenshots).

```
.venv\Scripts\python.exe day-30-portfolio-site\build_site.py
```

That writes a self-contained `docs/` folder. GitHub Pages serves `docs/`
straight from the main branch, so what you push is what goes live.

## Files

```
build_site.py        static site generator (writes docs/)
fun_facts.py         curated per-project fun facts
portfolio_schema.py  the project catalogue (day, name, tagline, stack, tags)
portfolio_engine.py  scans each folder for build status, tests, screenshots
pipeline.py          ties the scan together
server.py            optional local preview (Flask, port 1030)
templates/           index.html and project.html, shared by builder and preview
static/              style.css, app.js (the tag filter), favicon.svg
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
least two), and the no-dashes rule across the whole tree.
