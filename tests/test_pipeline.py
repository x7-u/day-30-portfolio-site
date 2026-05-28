"""Day 30 pipeline tests."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline import analyse

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_analyse_runs():
    a = analyse(PROJECT_ROOT, skip_ai=True)
    assert a.result is not None
    assert a.ai_cache is not None


def test_each_project_gets_talking_points():
    a = analyse(PROJECT_ROOT, skip_ai=True)
    for s in a.result.summaries:
        folder = s.project.folder
        assert folder in a.ai_cache.points
        assert len(a.ai_cache.points[folder]) == 3


def test_to_dict_json_serialisable():
    a = analyse(PROJECT_ROOT, skip_ai=True)
    blob = json.dumps(a.to_dict())
    assert "summaries" in blob
    assert "talking_points" in blob


def test_summaries_carry_talking_points_in_dict():
    a = analyse(PROJECT_ROOT, skip_ai=True)
    d = a.to_dict()
    has_points = sum(1 for s in d["summaries"]
                      if s.get("talking_points") and len(s["talking_points"]) == 3)
    assert has_points == len(d["summaries"])


def test_skip_ai_uses_fallback_provider():
    a = analyse(PROJECT_ROOT, skip_ai=True)
    assert a.ai_cache.provider == "fallback"


def test_total_counts_consistent():
    a = analyse(PROJECT_ROOT, skip_ai=True)
    assert a.result.total_projects == len(a.result.summaries)
    assert a.result.built_projects <= a.result.total_projects
