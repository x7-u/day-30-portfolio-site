"""Day 30 project-brief extraction tests.

The brief is pulled from each project's PROJECT_OVERVIEW.docx at build time.
Disk- and docx-dependent checks only run when the source files are present
(they are in the monorepo, not in the standalone published repo).
"""
from __future__ import annotations

from pathlib import Path

from project_brief import brief_for

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_brief_none_for_unknown():
    # A folder with neither a docx nor a curated brief yields None.
    assert brief_for(PROJECT_ROOT / "day-98-does-not-exist") is None


def test_manual_brief_for_days_without_docx():
    # Days 1 and 2 have no PROJECT_OVERVIEW.docx; a curated brief stands in.
    for folder in ("day-01-ratio-dashboard", "day-02-invoice-extractor"):
        b = brief_for(PROJECT_ROOT / folder)
        assert b is not None, folder
        assert b["facts"] and b["how_it_works"] and b["limitations"]
        blob = repr(b)
        assert chr(0x2014) not in blob and chr(0x2013) not in blob


def test_brief_extracts_when_present():
    folder = PROJECT_ROOT / "day-24-ddm-valuation"
    if not (folder / "PROJECT_OVERVIEW.docx").is_file():
        return
    try:
        import docx  # noqa: F401
    except ImportError:
        return
    b = brief_for(folder)
    assert b is not None
    assert b["facts"] and b["how_it_works"]
    assert b["walkthrough"] and b["limitations"]
    assert all("label" in f and "value" in f for f in b["facts"])
    assert all(it["title"] and it["summary"] for it in b["how_it_works"])
    # No em / en dashes leak in from the source document.
    blob = repr(b)
    assert chr(0x2014) not in blob and chr(0x2013) not in blob
