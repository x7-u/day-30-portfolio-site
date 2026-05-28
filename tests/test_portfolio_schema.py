"""Day 30 portfolio schema tests."""
from __future__ import annotations

from portfolio_schema import CATALOG


def test_catalog_has_29_entries():
    """Day 30 doesn't include itself."""
    assert len(CATALOG) == 29


def test_each_project_has_required_fields():
    for p in CATALOG:
        assert p.day > 0
        assert p.folder.startswith("day-")
        assert p.name
        assert p.tagline
        assert p.description
        assert p.stack
        assert p.tags
        assert p.port > 0


def test_ports_unique():
    ports = [p.port for p in CATALOG]
    assert len(ports) == len(set(ports))


def test_days_unique_and_sequential():
    days = [p.day for p in CATALOG]
    assert days == sorted(days)
    assert len(days) == len(set(days))


def test_folder_matches_day_number():
    for p in CATALOG:
        prefix = f"day-{p.day:02d}-"
        assert p.folder.startswith(prefix), f"day {p.day}: {p.folder}"


def test_all_have_accounting_focus():
    for p in CATALOG:
        assert p.accounting_focus, f"day {p.day} missing accounting_focus"


def test_all_have_ai_integration():
    for p in CATALOG:
        assert p.ai_integration, f"day {p.day} missing ai_integration"


def test_round_trip_to_dict():
    p = CATALOG[0]
    d = p.to_dict()
    assert d["day"] == p.day
    assert d["folder"] == p.folder
