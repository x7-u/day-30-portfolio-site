"""Day 30. Portfolio showcase server. Port 1030."""
from __future__ import annotations

import argparse
import logging
import logging.handlers
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask, abort, jsonify, render_template, request, send_file
from pipeline import analyse
from werkzeug.utils import safe_join

from shared.config import DEEPSEEK_API_KEY

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
LOGS = HERE / "logs"

app = Flask(__name__,
             template_folder=str(HERE / "templates"),
             static_folder=str(HERE / "static"))
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024

LOGS.mkdir(parents=True, exist_ok=True)
_handler = logging.handlers.RotatingFileHandler(
    LOGS / "server.log", maxBytes=512_000, backupCount=3, encoding="utf-8",
)
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler, logging.StreamHandler()])
log = logging.getLogger("day30.server")

# Cache the analysis on first request so the page is fast
_cache = {}


def _env_key_ok() -> bool:
    return bool(DEEPSEEK_API_KEY) and not DEEPSEEK_API_KEY.startswith("sk-placeholder")


def _safe_folder(name: str) -> bool:
    return bool(re.fullmatch(r"day-\d{2}-[a-z0-9-]+", name))


def _safe_file(name: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Z0-9_.\-]+\.png", name))


def _get_portfolio(skip_ai: bool = True):
    cache_key = "with_ai" if not skip_ai else "no_ai"
    if cache_key not in _cache:
        _cache[cache_key] = analyse(PROJECT_ROOT, skip_ai=skip_ai)
    return _cache[cache_key]


@app.route("/")
def index():
    skip_ai = request.args.get("ai", "off") != "on"
    portfolio = _get_portfolio(skip_ai=skip_ai)
    return render_template(
        "index.html",
        env_key_ok=_env_key_ok(),
        portfolio=portfolio.to_dict(),
        ai_enabled=not skip_ai,
    )


@app.route("/project/<folder>")
def project_detail(folder: str):
    if not _safe_folder(folder):
        abort(400)
    portfolio = _get_portfolio(skip_ai=True)
    project = None
    for s in portfolio.result.summaries:
        if s.project.folder == folder:
            project = s
            break
    if project is None:
        abort(404)
    proj_d = project.to_dict()
    # Pull talking points from AI cache (if available)
    if portfolio.ai_cache and folder in portfolio.ai_cache.points:
        proj_d["talking_points"] = portfolio.ai_cache.points[folder]
    return render_template(
        "project.html",
        env_key_ok=_env_key_ok(),
        project=proj_d,
    )


@app.route("/api/portfolio")
def api_portfolio():
    skip_ai = request.args.get("ai", "off") != "on"
    portfolio = _get_portfolio(skip_ai=skip_ai)
    return jsonify(portfolio.to_dict())


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    _cache.clear()
    skip_ai = request.json.get("skip_ai", True) if request.is_json else True
    portfolio = _get_portfolio(skip_ai=skip_ai)
    return jsonify({"refreshed": True, "total": portfolio.result.total_projects})


@app.route("/shots/<folder>/<filename>")
def serve_shot(folder: str, filename: str):
    if not _safe_folder(folder) or not _safe_file(filename):
        abort(400)
    safe = safe_join(str(PROJECT_ROOT), folder, "shots", filename)
    if not safe or not Path(safe).is_file():
        abort(404)
    return send_file(safe, mimetype="image/png")


@app.errorhandler(413)
def too_large(_e):
    return jsonify(error="Request too large."), 413


@app.route("/favicon.ico")
def favicon():
    p = HERE / "static" / "favicon.svg"
    if p.is_file():
        return send_file(p)
    return ("", 204)


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=int(os.getenv("DAY30_PORT", "1030")))
    p.add_argument("--debug", action="store_true")
    args = p.parse_args(argv)
    log.info("Day 30 Portfolio on http://%s:%s", args.host, args.port)
    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
