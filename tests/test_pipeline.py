"""Day 30 pipeline and fun-facts tests (static portfolio, no AI)."""
from __future__ import annotations

import json
from pathlib import Path

from fun_facts import FUN_FACTS, fun_facts_for
from pipeline import analyse
from portfolio_schema import CATALOG

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_analyse_returns_full_catalogue():
    a = analyse(PROJECT_ROOT)
    assert a.result is not None
    assert a.result.total_projects == len(CATALOG)
    assert a.result.summaries


def test_to_dict_json_serialisable_and_ai_free():
    blob = json.dumps(analyse(PROJECT_ROOT).to_dict())
    assert "summaries" in blob
    # The live AI is gone: no cache, no talking points.
    assert "ai_cache" not in blob
    assert "talking_points" not in blob


def test_every_project_has_at_least_two_fun_facts():
    a = analyse(PROJECT_ROOT)
    for s in a.result.summaries:
        facts = fun_facts_for(s)
        assert isinstance(facts, list) and len(facts) >= 2
        assert all(isinstance(f, str) and f.strip() for f in facts)


def test_curated_fun_facts_cover_the_whole_catalogue():
    for project in CATALOG:
        assert project.folder in FUN_FACTS, f"no fun facts for {project.folder}"
        assert len(FUN_FACTS[project.folder]) >= 2


def test_fun_facts_fallback_for_unknown_folder():
    class _Fake:
        folder = "day-99-unknown"
        name = "Mystery."
        stack = ["Python", "Flask"]
        accounting_focus = "Something useful"

    facts = fun_facts_for(_Fake())
    assert len(facts) == 2
    assert all(f.strip() for f in facts)


def test_total_counts_consistent():
    a = analyse(PROJECT_ROOT)
    assert a.result.total_projects == len(a.result.summaries)
    assert a.result.built_projects <= a.result.total_projects
