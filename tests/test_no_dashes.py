"""Day 18. Em / en dash byte scanner."""
from __future__ import annotations

import pathlib

DAY_ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTS = {".py", ".html", ".css", ".js", ".md"}
EM = b"\xe2\x80\x94"
EN = b"\xe2\x80\x93"
SELF = pathlib.Path(__file__).resolve()


def test_no_em_or_en_dashes():
    offenders = []
    for path in DAY_ROOT.rglob("*"):
        if path.suffix not in EXTS or path == SELF:
            continue
        if "__pycache__" in path.parts:
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        for i, line in enumerate(data.splitlines(), start=1):
            if EM in line or EN in line:
                snippet = line.decode("utf-8", errors="replace")[:80]
                offenders.append(f"{path.relative_to(DAY_ROOT)}:{i}: {snippet}")
    assert not offenders, "em / en dashes:\n" + "\n".join(offenders)
