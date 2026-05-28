"""Day 30. Portfolio talking-points AI.

For each project, the AI generates three talking points:
  - what accounting concept it demonstrates
  - what was learned technically
  - how it would extend in a professional context
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

log = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an interview coach helping a finance graduate
talk about their portfolio of 30 daily Python projects. For each
project, the graduate has 60 seconds to talk and needs three points: the
accounting concept demonstrated, the technical lesson learned, and the
extension into a professional context.

Plain English, first person ("I built", "I learned"). No marketing
language. Be specific about the accounting (cite IFRS, ACCA, ICAEW
where it fits) and the technology (cite the Python stack used).

Return STRICT JSON. Shape:

{
  "talking_points": [
    "string 1 - the accounting concept",
    "string 2 - the technical lesson",
    "string 3 - the professional extension"
  ]
}

Conventions:
- Exactly three talking points.
- Each 25-50 words.
- No em or en dashes.
"""


@dataclass
class CallStats:
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    model: str = ""
    cache_hit_tokens: int = 0
    latency_ms: int = 0


@dataclass
class AICache:
    """Caches generated talking points by project folder."""
    points: dict[str, list[str]] = field(default_factory=dict)
    stats: CallStats = field(default_factory=CallStats)
    provider: str = "fallback"

    def to_dict(self) -> dict:
        return {
            "points": self.points,
            "provider": self.provider,
            "stats": {
                "input_tokens": self.stats.input_tokens,
                "output_tokens": self.stats.output_tokens,
                "cost_usd": self.stats.cost_usd,
                "model": self.stats.model,
                "cache_hit_tokens": self.stats.cache_hit_tokens,
                "latency_ms": self.stats.latency_ms,
            },
        }


def _fallback_for(project) -> list[str]:
    """Templated three points based on project metadata."""
    return [
        f"I demonstrated {project.accounting_focus.lower()} by building a "
        f"working {project.name.replace('.', '').strip()} that takes "
        f"realistic inputs and produces a defensible output. The maths is "
        f"in Python, the AI explains, the audit trail is in Excel.",

        f"Technically I used {', '.join(project.stack[:3])} to ship a Flask "
        f"app on a local port. I learned how to structure a typed dataclass "
        f"schema, write tests against it, and embed matplotlib charts into "
        f"openpyxl workbooks without holding files open.",

        f"In a professional context I would extend this to integrate with "
        f"an ERP or accounting system, scale to multi-entity, and put the "
        f"AI prompt behind a versioned template store so the prose stays "
        f"consistent across teams.",
    ]


def generate(project, *, api_key: str | None = None,
              model: str | None = None,
              timeout: float = 30.0) -> tuple[list[str], CallStats, str]:
    """Return (talking_points, stats, provider) for one project."""
    key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
    if not key:
        return _fallback_for(project), CallStats(), "fallback"
    try:
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parent
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from shared.deepseek_client import ask_deepseek_json_with_stats
    except ImportError as e:
        log.warning("deepseek client unavailable: %s", e)
        return _fallback_for(project), CallStats(), "fallback"

    user_prompt = (
        f"Project: {project.name} - {project.tagline}\n"
        f"Day: {project.day}\n"
        f"Description: {project.description}\n"
        f"Stack: {', '.join(project.stack)}\n"
        f"Accounting focus: {project.accounting_focus}\n"
        f"AI integration: {project.ai_integration}\n\n"
        "Write the three talking points per the system instructions."
    )
    try:
        data, stats = ask_deepseek_json_with_stats(
            user_prompt, system=SYSTEM_PROMPT, max_tokens=800,
            model=model, api_key=key, timeout=timeout,
        )
    except Exception as e:  # noqa: BLE001
        log.warning("DeepSeek call failed: %s", e)
        return _fallback_for(project), CallStats(), "fallback"

    points = list(data.get("talking_points") or [])
    if len(points) != 3:
        return _fallback_for(project), CallStats(), "fallback"
    call_stats = CallStats(
        input_tokens=getattr(stats, "input_tokens", 0),
        output_tokens=getattr(stats, "output_tokens", 0),
        cost_usd=getattr(stats, "cost_usd", 0.0),
        model=getattr(stats, "model", model or ""),
        cache_hit_tokens=getattr(stats, "cache_hit_tokens", 0),
        latency_ms=getattr(stats, "latency_ms", 0),
    )
    return points, call_stats, "deepseek"


def generate_all(projects, *, api_key: str | None = None,
                  model: str | None = None,
                  skip_ai: bool = False) -> AICache:
    """Generate talking points for every project. Returns an AICache."""
    out = AICache()
    total_cost = 0.0
    total_in = 0
    total_out = 0
    providers_seen = set()
    for project in projects:
        if skip_ai:
            points = _fallback_for(project)
            stats = CallStats()
            provider = "fallback"
        else:
            points, stats, provider = generate(
                project, api_key=api_key, model=model)
        out.points[project.folder] = points
        total_cost += stats.cost_usd
        total_in += stats.input_tokens
        total_out += stats.output_tokens
        providers_seen.add(provider)
    out.stats = CallStats(
        input_tokens=total_in, output_tokens=total_out,
        cost_usd=total_cost,
        model="deepseek-v4" if "deepseek" in providers_seen else "",
    )
    out.provider = "deepseek" if "deepseek" in providers_seen else "fallback"
    return out
