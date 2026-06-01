"""Day 30 portfolio engine tests."""
from __future__ import annotations

from pathlib import Path

from portfolio_engine import _readme_top, build_portfolio, scan
from portfolio_schema import CATALOG

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# The sibling day-NN folders are present in the monorepo but not in the
# standalone published repo. Disk-dependent checks only run when they exist.
_HAS_DAY_FOLDERS = (PROJECT_ROOT / "day-01-ratio-dashboard").is_dir()


def test_scan_returns_summary_per_project():
    summaries = scan(PROJECT_ROOT)
    assert len(summaries) == len(CATALOG)


def test_built_projects_detected():
    """All days 1-29 should be detected as built (when the folders are here)."""
    if not _HAS_DAY_FOLDERS:
        return
    summaries = scan(PROJECT_ROOT)
    built_count = sum(1 for s in summaries if s.built)
    # At least 25 should be built (days 1-29 in this state)
    assert built_count >= 25


def test_tests_counted():
    """At least some projects should have tests counted."""
    if not _HAS_DAY_FOLDERS:
        return
    summaries = scan(PROJECT_ROOT)
    total = sum(s.test_count for s in summaries)
    assert total > 100  # we know we have hundreds across days


def test_readme_top_returns_substantive_paragraph():
    """For a project with a known README we get a non-trivial paragraph."""
    day24 = PROJECT_ROOT / "day-24-ddm-valuation"
    if not day24.is_dir():
        return
    top = _readme_top(day24)
    assert len(top) > 50


def test_build_portfolio_aggregates():
    portfolio = build_portfolio(PROJECT_ROOT)
    assert portfolio.total_projects == len(CATALOG)
    assert portfolio.tag_counts
    assert portfolio.stack_counts
    if _HAS_DAY_FOLDERS:
        assert portfolio.built_projects > 0
        assert portfolio.total_tests > 100


def test_tag_counts_match_catalog():
    portfolio = build_portfolio(PROJECT_ROOT)
    # Manually count tags from catalog and compare
    expected: dict[str, int] = {}
    for p in CATALOG:
        for t in p.tags:
            expected[t] = expected.get(t, 0) + 1
    assert portfolio.tag_counts == expected
