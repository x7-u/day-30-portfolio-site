"""Day 30. Condensed brief for each project, shown on its detail page.

For days 3 to 29 the brief is pulled from the project's PROJECT_OVERVIEW.docx
at build time (faithful to the source, no AI, no runtime cost):

  - facts        the header key/value lines (use case, inputs, outputs, ...)
  - how_it_works the "How it works" component list (title + one-line summary)
  - walkthrough  the screenshot tour (frame title + caption)
  - limitations  the honest "Limitations" bullets

Days 1 and 2 predate the overview-doc format, so they use a curated brief in
``_MANUAL_BRIEFS`` (written from their READMEs). Parsing happens in the
monorepo, where the docx files and python-docx are available; the published
site just serves the baked HTML. Anything with neither a docx nor a curated
entry (or python-docx absent) yields ``None`` and the page omits the brief.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from docx import Document
except ImportError:  # standalone published repo may not have python-docx
    Document = None

# No em / en dashes anywhere in output (hard rule for this project). Built from
# code points so this source file itself stays free of the banned bytes.
_DASH = str.maketrans({chr(0x2014): "-", chr(0x2013): "-"})

# Section headings as they appear in the docs (lower-cased) -> internal key.
_SECTIONS = {
    "walk-through": "walkthrough",
    "how it works": "how_it_works",
    "limitations": "limitations",
    "limitations called out honestly": "limitations",
    "post-30 expansion": "post30",
    "post-30": "post30",
    "bottom line": "bottom_line",
}

# Only these header labels surface as facts (in this order). Everything else,
# including stack/port/tests/ai (shown elsewhere) and any prose that happens to
# contain a colon, is ignored. An allow-list keeps the block clean.
_FACT_ORDER = ["use case", "standard", "framework", "tiers",
               "engine", "universe", "edgar", "glossary size",
               "inputs", "outputs", "model", "cost"]
_FACT_LABELS = set(_FACT_ORDER)


def _clean(text: str) -> str:
    return " ".join(text.split()).translate(_DASH).strip()


def _trim(text: str, max_chars: int = 160) -> str:
    """First sentence only, cut on a word boundary."""
    first = re.split(r"(?<=[.!?])\s+", _clean(text))[0] if text.strip() else ""
    if len(first) > max_chars:
        first = first[:max_chars].rsplit(" ", 1)[0] + "..."
    return first.strip()


def _first_sentences(text: str, *, max_chars: int = 180) -> str:
    """First sentence, plus a second if the first is very short."""
    sents = [s for s in re.split(r"(?<=[.!?])\s+", _clean(text)) if s]
    out = sents[0] if sents else ""
    if len(out) < 45 and len(sents) > 1 and len(out) + 1 + len(sents[1]) <= max_chars:
        out = f"{out} {sents[1]}"
    if len(out) > max_chars:
        out = out[:max_chars].rsplit(" ", 1)[0] + "..."
    return out.strip()


def brief_for(folder: Path) -> dict | None:
    """Brief for a project folder: the docx if present, else a curated entry."""
    path = folder / "PROJECT_OVERVIEW.docx"
    if Document is not None and path.is_file():
        parsed = _parse_docx(path)
        if parsed:
            return parsed
    return _MANUAL_BRIEFS.get(folder.name)


def _parse_docx(path: Path) -> dict | None:
    try:
        doc = Document(str(path))
    except Exception:
        return None

    paras = []
    for p in doc.paragraphs:
        t = _clean(p.text)
        if not t:
            continue
        is_bullet = "List Bullet" in (p.style.name if p.style else "")
        paras.append((t, is_bullet))
    if not paras:
        return None

    marks = [(i, _SECTIONS[t.lower()]) for i, (t, _b) in enumerate(paras)
             if t.lower() in _SECTIONS]
    first_section = marks[0][0] if marks else len(paras)

    brief: dict = {
        "facts": _facts(paras[1:first_section]),
        "how_it_works": [],
        "walkthrough": [],
        "limitations": [],
    }
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(paras)
        body = paras[start + 1:end]
        if key == "how_it_works":
            brief["how_it_works"] = _how_it_works(body)
        elif key == "walkthrough":
            brief["walkthrough"] = _walkthrough(body)
        elif key == "limitations":
            brief["limitations"] = _limitations(body)

    if not any(brief[k] for k in
               ("facts", "how_it_works", "walkthrough", "limitations")):
        return None
    return brief


def _facts(rows) -> list[dict]:
    found: dict[str, tuple[str, str]] = {}
    for t, _b in rows:
        if ":" not in t:
            continue
        label, _, value = t.partition(":")
        key = label.strip().lower()
        if key not in _FACT_LABELS or key in found:
            continue
        value = _trim(value, 160)
        if value:
            found[key] = (label.strip(), value)
    return [{"label": found[k][0], "value": found[k][1]}
            for k in _FACT_ORDER if k in found][:6]


def _how_it_works(body) -> list[dict]:
    items: list[dict] = []
    title: str | None = None
    buf: list[str] = []

    def flush() -> None:
        if title:
            items.append({"title": title.rstrip(":").strip(),
                          "summary": _first_sentences(" ".join(buf))})

    for t, _b in body:
        if t.endswith(":") and len(t) < 45:
            flush()
            title, buf = t, []
        else:
            buf.append(t)
    flush()
    return [x for x in items if x["title"] and x["summary"]][:6]


def _walkthrough(body) -> list[dict]:
    frames: list[dict] = []
    title: str | None = None
    caption: str | None = None
    for t, _b in body:
        if re.match(r"^\d+[.)]\s", t):
            if title:
                frames.append({"title": title, "caption": caption or ""})
            title = _clean(re.sub(r"^\d+[.)]\s*", "", t))
            caption = None
        elif title and caption is None:
            caption = _first_sentences(t, max_chars=120)
    if title:
        frames.append({"title": title, "caption": caption or ""})
    return frames[:6]


def _limitations(body) -> list[str]:
    out = [_first_sentences(t.lstrip("-* ").strip())
           for t, is_bullet in body if is_bullet or t[:1] in "-*"]
    if not out:  # bullets weren't styled; fall back to plain paragraphs
        out = [_first_sentences(t) for t, _b in body]
    return [x for x in out if x][:6]


# ------------------------------------------------------------
# Curated briefs for the days that have no PROJECT_OVERVIEW.docx
# (days 1 and 2 predate that format). Written from their READMEs
# in the same shape the docx parser produces.
# ------------------------------------------------------------
_MANUAL_BRIEFS: dict[str, dict] = {
    "day-01-ratio-dashboard": {
        "facts": [
            {"label": "Use case",
             "value": "Financial-statement analysis, SME ratio review with "
                      "director commentary"},
            {"label": "Inputs",
             "value": "A company's two-period income statement and balance "
                      "sheet (.xlsx); several files for multi-company comparison"},
            {"label": "Outputs",
             "value": "24 ratios with sector-aware RAG flags, AI commentary, "
                      "and a self-contained Excel dashboard"},
            {"label": "Model",
             "value": "Claude Haiku 4.5 default, Sonnet 4.6 / Opus 4.7 selectable"},
            {"label": "Cost",
             "value": "around $0.0025 per run on Haiku 4.5, $0 with --no-ai"},
        ],
        "how_it_works": [
            {"title": "Ratio engine",
             "summary": "ratios.py computes 24 ratios across liquidity, "
                        "solvency, profitability and efficiency, then classifies "
                        "each red / amber / green against dataclass thresholds."},
            {"title": "Sector profiles",
             "summary": "sectors.py overrides the thresholds for retail, "
                        "manufacturing, services and SaaS so the RAG bands match "
                        "the business model."},
            {"title": "AI commentary",
             "summary": "pipeline.py sends a compact pipe-delimited digest of the "
                        "ratios to Claude, which writes a finance-director "
                        "commentary; an offline --no-ai mode skips the call."},
            {"title": "Excel output",
             "summary": "excel_writer.py renders a dashboard with sortable numeric "
                        "cells, RAG-coloured pills, an embedded chart and A4 print "
                        "setup."},
        ],
        "walkthrough": [],
        "limitations": [
            "Two-period analysis. Historical trend charting beyond two years is "
            "post-30.",
            "No peer benchmarking. Sector averages from Companies House or public "
            "filings are post-30.",
            "AI commentary is a draft. It is grounded in the computed ratios but "
            "should be reviewed before use.",
            "Local-only. Loopback Flask dev server with no auth; production "
            "hosting is a later step.",
        ],
    },
    "day-02-invoice-extractor": {
        "facts": [
            {"label": "Use case",
             "value": "Accounts-payable automation, invoice data capture from "
                      "PDFs and images"},
            {"label": "Inputs",
             "value": "Invoice PDFs or images (jpg / png / webp); multi-page PDFs "
                      "capped at 5 pages"},
            {"label": "Outputs",
             "value": "CSV (one row per line item), a multi-sheet Excel workbook, "
                      "and a per-invoice confidence band and duplicate flag"},
            {"label": "Model",
             "value": "Claude Haiku 4.5 vision default, Sonnet 4.6 / Opus 4.7 "
                      "selectable"},
            {"label": "Cost",
             "value": "around $0.003 to $0.005 per invoice on Haiku 4.5, $0 with "
                      "--no-ai"},
        ],
        "how_it_works": [
            {"title": "Page rasteriser",
             "summary": "pdf_loader.py turns each PDF or image page into image "
                        "bytes with pypdfium2 and Pillow (EXIF-rotate, clamp to a "
                        "1568px edge)."},
            {"title": "Vision extraction",
             "summary": "pipeline.py sends each page to Claude's vision API and "
                        "gets strict JSON back: vendor, invoice number, dates, "
                        "line items, subtotal, tax, currency and a confidence band."},
            {"title": "Arithmetic validation",
             "summary": "invoice_schema.py checks line items sum to subtotal and "
                        "subtotal plus tax equals total; mismatches add warnings "
                        "and downgrade confidence rather than silently correcting."},
            {"title": "Duplicate ledger",
             "summary": "ledger.py fingerprints every extraction (vendor, number, "
                        "date, currency, total) and flags re-uploads as EXACT, "
                        "SUSPICIOUS or FUZZY."},
            {"title": "CSV + Excel output",
             "summary": "one accountant-friendly row per line item, plus an "
                        "Invoices / Line items / Summary workbook with an embedded "
                        "chart and confidence pills."},
        ],
        "walkthrough": [],
        "limitations": [
            "AI proposes, you decide. Validation surfaces discrepancies but never "
            "silently corrects the model's numbers.",
            "Multi-page PDFs are capped at 5 pages per file; over-cap files "
            "trigger a warning.",
            "Generic CSV export. Direct Xero / QuickBooks / Sage import formats "
            "are post-30.",
            "No on-device OCR fallback. Offline runs produce stub output; a "
            "Tesseract fallback is post-30.",
            "Local-only. Loopback Flask dev server with no auth; production "
            "hosting is a later step.",
        ],
    },
}
