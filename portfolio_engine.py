"""Day 30. Portfolio scan engine.

Walks each project folder and gathers metadata:
  - whether the project has been built (has a server.py)
  - whether tests pass count exists
  - first screenshot path
  - top of README
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from portfolio_schema import CATALOG, Project


@dataclass
class ProjectSummary:
    project: Project
    built: bool = False
    screenshot_count: int = 0
    has_excel_writer: bool = False
    has_tests: bool = False
    test_count: int = 0
    readme_top: str = ""

    def to_dict(self) -> dict:
        d = self.project.to_dict()
        d.update({
            "built": self.built,
            "screenshot_count": self.screenshot_count,
            "has_excel_writer": self.has_excel_writer,
            "has_tests": self.has_tests,
            "test_count": self.test_count,
            "readme_top": self.readme_top,
        })
        return d


def _readme_top(folder: Path) -> str:
    p = folder / "README.md"
    if not p.is_file():
        return ""
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return ""
    # Skip the title line, take the first non-empty paragraph
    lines = text.splitlines()
    paras: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip().startswith("#"):
            if current:
                paras.append(" ".join(current).strip()); current = []
            continue
        if not line.strip():
            if current:
                paras.append(" ".join(current).strip()); current = []
            continue
        current.append(line.strip())
    if current:
        paras.append(" ".join(current).strip())
    # First substantive paragraph
    for p_ in paras:
        if len(p_) > 50:
            return p_[:600]
    return paras[0] if paras else ""


def _count_tests(folder: Path) -> int:
    test_dir = folder / "tests"
    if not test_dir.is_dir():
        return 0
    n = 0
    for p in test_dir.glob("test_*.py"):
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        n += len(re.findall(r"^def test_\w+", text, re.MULTILINE))
    return n


def _screenshots(folder: Path) -> list[str]:
    shots_dir = folder / "shots"
    if not shots_dir.is_dir():
        return []
    return sorted(p.name for p in shots_dir.glob("*.png"))


def scan(project_root: Path) -> list[ProjectSummary]:
    """Return a summary for every project in the catalog."""
    summaries: list[ProjectSummary] = []
    for project in CATALOG:
        folder = project_root / project.folder
        if not folder.is_dir():
            summaries.append(ProjectSummary(
                project=project, built=False,
                readme_top="(folder not on disk)"))
            continue
        server_py = folder / "server.py"
        excel_py = folder / "excel_writer.py"
        shots = _screenshots(folder)
        # Copy shots list into project so the AI sees them
        project.shots = shots
        summaries.append(ProjectSummary(
            project=project,
            built=server_py.is_file(),
            screenshot_count=len(shots),
            has_excel_writer=excel_py.is_file(),
            has_tests=(folder / "tests").is_dir(),
            test_count=_count_tests(folder),
            readme_top=_readme_top(folder),
        ))
    return summaries


@dataclass
class PortfolioResult:
    summaries: list[ProjectSummary] = field(default_factory=list)
    total_projects: int = 0
    built_projects: int = 0
    total_tests: int = 0
    total_screenshots: int = 0
    tag_counts: dict[str, int] = field(default_factory=dict)
    stack_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "summaries": [s.to_dict() for s in self.summaries],
            "total_projects": self.total_projects,
            "built_projects": self.built_projects,
            "total_tests": self.total_tests,
            "total_screenshots": self.total_screenshots,
            "tag_counts": self.tag_counts,
            "stack_counts": self.stack_counts,
        }


def build_portfolio(project_root: Path) -> PortfolioResult:
    summaries = scan(project_root)
    tag_counts: dict[str, int] = {}
    stack_counts: dict[str, int] = {}
    for s in summaries:
        for t in s.project.tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
        for st in s.project.stack:
            stack_counts[st] = stack_counts.get(st, 0) + 1
    return PortfolioResult(
        summaries=summaries,
        total_projects=len(summaries),
        built_projects=sum(1 for s in summaries if s.built),
        total_tests=sum(s.test_count for s in summaries),
        total_screenshots=sum(s.screenshot_count for s in summaries),
        tag_counts=tag_counts,
        stack_counts=stack_counts,
    )
