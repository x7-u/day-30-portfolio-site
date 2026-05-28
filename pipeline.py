"""Day 30. Portfolio orchestrator."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

from portfolio_ai import AICache, generate_all
from portfolio_engine import PortfolioResult, build_portfolio

log = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    result: PortfolioResult
    ai_cache: AICache | None = None
    elapsed_ms: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = self.result.to_dict()
        # Merge AI points into each summary
        if self.ai_cache:
            points = self.ai_cache.points
            for s in d["summaries"]:
                folder = s.get("folder")
                if folder in points:
                    s["talking_points"] = points[folder]
        d["ai_cache"] = self.ai_cache.to_dict() if self.ai_cache else None
        d["elapsed_ms"] = self.elapsed_ms
        d["warnings"] = self.warnings
        return d


def analyse(project_root: Path, *,
            skip_ai: bool = False,
            api_key: str | None = None, model: str | None = None
            ) -> AnalysisResult:
    t0 = time.monotonic()
    portfolio = build_portfolio(project_root)
    projects = [s.project for s in portfolio.summaries]
    ai_cache = generate_all(projects, skip_ai=skip_ai,
                              api_key=api_key, model=model)
    elapsed = int((time.monotonic() - t0) * 1000)
    return AnalysisResult(
        result=portfolio, ai_cache=ai_cache,
        elapsed_ms=elapsed, warnings=[],
    )
