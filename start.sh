#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
PORT="${1:-1030}"
PY="../.venv/bin/python"
[ -x "$PY" ] || PY="../.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
echo "Starting Day 30 Portfolio. on http://127.0.0.1:${PORT}/"
"$PY" server.py --port "$PORT"
