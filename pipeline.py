"""Day 30. Portfolio orchestrator.

This is a static portfolio: it scans the project folders and builds the
catalogue. There is no AI call at view time. Each project's fun facts are
curated in ``fun_facts.py`` and added by the server (and the static builder)
when a page is rendered.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from portfolio_engine import PortfolioResult, build_portfolio


@dataclass
class AnalysisResult:
    result: PortfolioResult
    elapsed_ms: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = self.result.to_dict()
        d["elapsed_ms"] = self.elapsed_ms
        d["warnings"] = self.warnings
        return d


def analyse(project_root: Path) -> AnalysisResult:
    """Scan the project folders and return the portfolio catalogue."""
    t0 = time.monotonic()
    portfolio = build_portfolio(project_root)
    elapsed = int((time.monotonic() - t0) * 1000)
    return AnalysisResult(result=portfolio, elapsed_ms=elapsed)
