"""Day 30 personal-projects + category tests."""
from __future__ import annotations

import re
from pathlib import Path

from portfolio_engine import all_summaries, home_context, personal_summaries
from portfolio_schema import CATALOG, PERSONAL
from project_brief import brief_for

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_finance_catalog_unchanged():
    assert len(CATALOG) == 29
    assert all(p.category == "finance" for p in CATALOG)


def test_personal_projects_shape():
    assert len(PERSONAL) == 5
    for p in PERSONAL:
        assert p.category == "personal"
        assert p.repo.startswith("https://github.com/x7-u/")
        # The folder doubles as the URL slug, so it must be url-safe.
        assert re.fullmatch(r"[a-z0-9][a-z0-9-]+", p.folder), p.folder
        assert p.name and p.tagline and p.description and p.stack


def test_personal_summaries():
    ps = personal_summaries()
    assert len(ps) == 5
    assert all(s.project.category == "personal" for s in ps)
    assert all(s.test_count == 0 and s.screenshot_count == 0 for s in ps)


def test_personal_projects_have_briefs():
    # Each personal project now carries a curated brief (from its README).
    for p in PERSONAL:
        b = brief_for(PROJECT_ROOT / p.folder)
        assert b is not None, p.folder
        assert b["how_it_works"], p.folder
        blob = repr(b)
        assert chr(0x2014) not in blob and chr(0x2013) not in blob


def test_home_context_counts():
    ctx = home_context(all_summaries(PROJECT_ROOT))
    assert ctx["total_projects"] == len(CATALOG) + len(PERSONAL)
    assert ctx["finance_count"] == len(CATALOG)
    assert ctx["personal_count"] == len(PERSONAL)
    # Every card carries a category the front-end can filter on.
    assert all(c["category"] in ("finance", "personal") for c in ctx["summaries"])
