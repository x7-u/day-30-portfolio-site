"""Day 30 test isolation."""
from __future__ import annotations

import sys
from pathlib import Path

DAY_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DAY_ROOT.parent

_CONFLICTING = {
    "excel_writer", "pipeline", "csv_writer", "ratios", "sectors",
    "pdf_loader", "invoice_schema", "main", "server", "ledger",
    "variance", "budget_schema", "cost_log", "pptx_writer", "pdf_writer",
    "history_store", "comparison", "run_cache", "power_bi",
    "cashflow_schema", "cashflow_maths", "scenario",
    "news_schema", "aggregation", "sentiment", "chart",
    "corrections", "live_fetcher", "industries",
    "pulse_pptx", "pulse_pdf",
    "cvp_schema", "cvp_maths", "cvp_chart", "cvp_excel", "cvp_csv",
    "break_pptx", "break_pdf", "monte_carlo", "benchmarks",
    "transcript_schema", "analysis", "hedge_phrases", "claims",
    "brief_chart",
    "statement_schema", "merchant_dict", "categoriser", "stats", "pdf_parser",
    "dcf_maths", "sensitivity", "assumption_schema", "ai_prefill",
    "ap_schema", "ageing", "ai_flagger", "db",
    "edgar", "xbrl_parser", "filing_parser", "financials", "risk_extractor",
    "asset_universe", "portfolio_schema", "simulator", "risk_metrics",
    "ai_commentator",
    "tb_schema", "pl_compute", "bs_compute", "cf_compute", "kpi_compute",
    "yoy_compute",
    "glossary", "jargon_finder", "doc_type", "ai_explainer",
    "inventory_schema", "inventory_metrics", "eoq_calculator",
    "ai_recommender",
    "lease_schema", "ifrs16_maths",
    "tax_schema", "tax_maths", "rd_identifier",
    "score_schema", "score_maths", "credit_memo",
    "fx_schema", "fx_maths", "hedging_ai",
    "report_schema", "report_builder", "narrative_ai", "docx_writer",
    "wc_schema", "wc_maths", "wc_ai",
    "wacc_schema", "wacc_maths", "wacc_ai",
    "fraud_schema", "fraud_engine", "fraud_ai",
    "ddm_schema", "ddm_maths", "ddm_ai",
    "coa_schema", "coa_maths", "coa_ai",
    "research_schema", "research_maths", "research_ai",
    "payroll_schema", "payroll_engine", "payroll_ai",
    "valuation_schema", "valuation_maths", "valuation_ai",
    "chat_schema", "chat_engine", "chat_ai",
    # Day 30
    "portfolio_engine", "portfolio_ai",
}


def _evict_and_set_path() -> None:
    for name in list(_CONFLICTING):
        sys.modules.pop(name, None)
    for p in (str(DAY_ROOT), str(PROJECT_ROOT)):
        if p in sys.path:
            sys.path.remove(p)
    sys.path.insert(0, str(DAY_ROOT))
    sys.path.insert(0, str(PROJECT_ROOT))


_evict_and_set_path()


def pytest_collectstart(collector):
    p = getattr(collector, "path", None) or getattr(collector, "fspath", None)
    if p is None:
        return
    if str(DAY_ROOT) in str(p):
        _evict_and_set_path()


import pytest


@pytest.fixture(autouse=True)
def _ensure_day_path():
    _evict_and_set_path()
    yield


for p in (str(DAY_ROOT), str(PROJECT_ROOT)):
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, str(DAY_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))
