"""Day 30. Portfolio project catalog and per-project metadata."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Project:
    day: int
    folder: str
    name: str            # short display name (e.g. "Cycle.")
    tagline: str         # one-line tagline
    description: str     # 2-3 sentence description
    stack: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)   # filter chips
    port: int = 0
    accounting_focus: str = ""
    ai_integration: str = ""
    shots: list[str] = field(default_factory=list)            # screenshot rel paths

    def to_dict(self) -> dict:
        return {
            "day": self.day, "folder": self.folder,
            "name": self.name, "tagline": self.tagline,
            "description": self.description,
            "stack": list(self.stack), "tags": list(self.tags),
            "port": self.port,
            "accounting_focus": self.accounting_focus,
            "ai_integration": self.ai_integration,
            "shots": list(self.shots),
        }


# ============================================================
# Static catalog (Day 30 is the live index of Days 1 to 29).
# ============================================================

CATALOG: list[Project] = [
    Project(
        day=1, folder="day-01-ratio-dashboard",
        name="Ratio Dashboard",
        tagline="Financial ratio analysis with AI commentary",
        description="Drop in financial statements; the engine computes "
                     "liquidity, profitability and gearing ratios with RAG "
                     "flags, and Claude writes the controller commentary.",
        stack=["Python", "Flask", "openpyxl", "Anthropic"],
        tags=["ratios", "ai-commentary", "excel"],
        port=1001,
        accounting_focus="Financial statement analysis",
        ai_integration="Claude writes the management commentary",
    ),
    Project(
        day=2, folder="day-02-invoice-extractor",
        name="Invoice Workbench",
        tagline="PDF invoice extraction to ledger CSV",
        description="Drag PDF or image invoices in; the AI extracts line "
                     "items, totals and counterparty into a normalised "
                     "ledger. Confidence scores and an audit trail per line.",
        stack=["Python", "Flask", "pdf parsing", "Anthropic"],
        tags=["ocr", "ap", "automation"],
        port=1002,
        accounting_focus="Accounts payable automation",
        ai_integration="Claude extracts and normalises invoice fields",
    ),
    Project(
        day=3, folder="day-03-budget-tracker",
        name="Budget vs Actual",
        tagline="Variance tracking with management commentary",
        description="Budget and actual side-by-side with per-row tolerance, "
                     "direction-aware adverse vs favourable, and AI-drafted "
                     "management commentary.",
        stack=["Python", "Flask", "openpyxl", "Anthropic"],
        tags=["budget", "variance", "rag"],
        port=1003,
        accounting_focus="Budget control and management reporting",
        ai_integration="Claude drafts the period commentary",
    ),
    Project(
        day=4, folder="day-04-cashflow-model",
        name="Cashflow Model",
        tagline="13-week cash flow forecast with scenario engine",
        description="Drop in receipts, payments, payroll and tax; the engine "
                     "builds a rolling 13-week balance projection. DeepSeek "
                     "V4 parses 'what if' prompts into deterministic shocks.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["cashflow", "treasury", "scenario"],
        port=1004,
        accounting_focus="Treasury and short-term liquidity",
        ai_integration="DeepSeek parses scenarios + writes commentary",
    ),
    Project(
        day=5, folder="day-05-sentiment-analyser",
        name="Sentiment Pulse",
        tagline="Financial news sentiment with sector aggregation",
        description="Ingests news headlines; classifies sentiment per "
                     "company and rolls up to sector. Bias-aware aggregation, "
                     "RAG flags on extreme movements.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["sentiment", "news", "nlp"],
        port=1005,
        accounting_focus="Market context for investment analysis",
        ai_integration="DeepSeek classifies headline sentiment",
    ),
    Project(
        day=6, folder="day-06-breakeven-tool",
        name="Breakeven Tool",
        tagline="Cost-volume-profit analysis with Monte Carlo",
        description="Compute break-even volume and revenue from fixed costs, "
                     "variable costs and price. Monte Carlo overlay shows "
                     "the probability distribution of profit.",
        stack=["Python", "Flask", "numpy", "matplotlib"],
        tags=["cvp", "breakeven", "mc"],
        port=1006,
        accounting_focus="Cost accounting and pricing decisions",
        ai_integration="DeepSeek interprets break-even output",
    ),
    Project(
        day=7, folder="day-07-earnings-summariser",
        name="Earnings Brief",
        tagline="Earnings transcript analysis and claim extraction",
        description="Drop in an earnings call transcript; AI extracts the "
                     "forward-looking statements, hedge phrases, and claims "
                     "with confidence scoring.",
        stack=["Python", "Flask", "DeepSeek"],
        tags=["earnings", "nlp", "ir"],
        port=1007,
        accounting_focus="Investor relations and disclosure",
        ai_integration="DeepSeek extracts hedge phrases and claims",
    ),
    Project(
        day=8, folder="day-08-finance-categoriser",
        name="Finance Categoriser",
        tagline="Bank statement categorisation",
        description="Drop in a bank statement; the engine categorises every "
                     "transaction by merchant dictionary plus AI for "
                     "edge cases.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["bank", "categorisation", "personal"],
        port=1008,
        accounting_focus="Personal and small-business bookkeeping",
        ai_integration="DeepSeek categorises ambiguous transactions",
    ),
    Project(
        day=9, folder="day-09-dcf-model",
        name="DCF Model",
        tagline="5-year DCF with sensitivity and Monte Carlo",
        description="Five-year free cash flow forecast with Gordon terminal, "
                     "5x5 sensitivity over WACC and growth, and a Monte "
                     "Carlo overlay for the intrinsic value distribution.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["valuation", "dcf", "mc"],
        port=1009,
        accounting_focus="Corporate valuation",
        ai_integration="DeepSeek writes the valuation commentary",
    ),
    Project(
        day=10, folder="day-10-ap-ageing-report",
        name="AP Ageing",
        tagline="Accounts payable ageing with AI flagger",
        description="Bucket-by-bucket ageing (0-30, 30-60, 60-90, 90+) "
                     "across suppliers, with AI flagging unusual delays.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["ap", "ageing", "treasury"],
        port=1010,
        accounting_focus="Accounts payable management",
        ai_integration="DeepSeek flags unusual ageing patterns",
    ),
    Project(
        day=11, folder="day-11-sec-filing-parser",
        name="Filing Parser",
        tagline="SEC 10-K parsing with risk extraction",
        description="Parse SEC 10-K filings from EDGAR; extract the risk "
                     "section, executive summary, and key financials.",
        stack=["Python", "Flask", "BeautifulSoup", "DeepSeek"],
        tags=["sec", "filings", "edgar"],
        port=1011,
        accounting_focus="Public-company disclosure analysis",
        ai_integration="DeepSeek extracts risk and forward-looking",
    ),
    Project(
        day=12, folder="day-12-monte-carlo-sim",
        name="Monte Carlo",
        tagline="Risk simulation for portfolio analysis",
        description="Run 10,000 simulations on a multi-asset portfolio "
                     "with configurable returns, volatility, correlations.",
        stack=["Python", "Flask", "numpy", "matplotlib"],
        tags=["risk", "mc", "portfolio"],
        port=1012,
        accounting_focus="Portfolio risk analysis",
        ai_integration="DeepSeek writes the risk commentary",
    ),
    Project(
        day=13, folder="day-13-mgmt-accounts",
        name="Mgmt Accounts",
        tagline="P&L, balance sheet and cash flow from trial balance",
        description="Take a trial balance, produce the three primary "
                     "statements with YoY comparison and AI commentary.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["financials", "tb", "trial-balance"],
        port=1013,
        accounting_focus="Management accounts production",
        ai_integration="DeepSeek writes the period commentary",
    ),
    Project(
        day=14, folder="day-14-jargon-explainer",
        name="Jargon Explainer",
        tagline="Glossary for finance jargon in any document",
        description="Drop in a finance document; AI finds the jargon, "
                     "explains it in plain English, builds a glossary.",
        stack=["Python", "Flask", "DeepSeek"],
        tags=["glossary", "training", "nlp"],
        port=1014,
        accounting_focus="Training and accessibility",
        ai_integration="DeepSeek identifies and explains jargon",
    ),
    Project(
        day=15, folder="day-15-inventory-optimiser",
        name="Inventory Optimiser",
        tagline="EOQ + reorder point + AI recommendations",
        description="Economic order quantity, reorder point, and safety "
                     "stock for inventory items with AI recommendations.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["inventory", "eoq", "supply-chain"],
        port=1015,
        accounting_focus="Inventory and working-capital management",
        ai_integration="DeepSeek recommends stocking levels",
    ),
    Project(
        day=16, folder="day-16-ifrs16-calculator",
        name="IFRS 16 Calculator",
        tagline="Right-of-use asset and lease liability schedule",
        description="Full IFRS 16 calculation: ROU asset, lease liability, "
                     "interest accrual, year-by-year schedule.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["ifrs", "lease", "compliance"],
        port=1016,
        accounting_focus="Lease accounting compliance",
        ai_integration="DeepSeek explains the journal flow",
    ),
    Project(
        day=17, folder="day-17-tax-provision",
        name="Tax Provision",
        tagline="Corporation tax computation with R&D identifier",
        description="UK corporation tax computation with deferred tax, "
                     "R&D identification, and effective rate calculation.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["tax", "rd", "provision"],
        port=1017,
        accounting_focus="Corporate tax accounting",
        ai_integration="DeepSeek flags R&D eligible spend",
    ),
    Project(
        day=18, folder="day-18-credit-scorecard",
        name="Credit Scorecard",
        tagline="Trade credit scorecard with memo writer",
        description="Score a counterparty on the standard 5-factor model "
                     "(liquidity, leverage, profitability, scale, payment "
                     "behaviour) and draft the credit memo.",
        stack=["Python", "Flask", "DeepSeek"],
        tags=["credit", "ar", "risk"],
        port=1018,
        accounting_focus="Credit risk assessment",
        ai_integration="DeepSeek drafts the credit memo",
    ),
    Project(
        day=19, folder="day-19-fx-exposure",
        name="FX Exposure",
        tagline="FX exposure analysis with hedging recommendations",
        description="Aggregate FX exposure by currency and tenor; AI "
                     "recommends hedging instruments and ratios.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["fx", "hedging", "treasury"],
        port=1019,
        accounting_focus="FX risk management",
        ai_integration="DeepSeek recommends hedging strategy",
    ),
    Project(
        day=20, folder="day-20-report-builder",
        name="Report Builder",
        tagline="Automated management reports from P&L plus KPIs",
        description="Generate a fully formatted Word document plus Excel "
                     "workbook of the management report from your P&L lines "
                     "and KPI dashboard.",
        stack=["Python", "Flask", "python-docx", "DeepSeek"],
        tags=["reporting", "docx", "automation"],
        port=1020,
        accounting_focus="Management reporting automation",
        ai_integration="DeepSeek writes the narrative sections",
    ),
    Project(
        day=21, folder="day-21-working-capital",
        name="Cycle.",
        tagline="Working capital DSO/DPO/DIO/CCC dashboard",
        description="Multi-period working capital diagnostics with sector "
                     "benchmarks. AI explains the trapped-cash impact.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["working-capital", "dso", "treasury"],
        port=1021,
        accounting_focus="Working capital management",
        ai_integration="DeepSeek writes trapped-cash commentary",
    ),
    Project(
        day=22, folder="day-22-wacc-calculator",
        name="WACC.",
        tagline="Cost of capital with sector beta checks",
        description="Build WACC step by step: CAPM cost of equity, after-tax "
                     "cost of debt, capital structure. AI sanity-checks "
                     "every input against sector typicals.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["wacc", "valuation", "capm"],
        port=1022,
        accounting_focus="Cost of capital",
        ai_integration="DeepSeek sanity-checks inputs",
    ),
    Project(
        day=23, folder="day-23-fraud-detection",
        name="Audit.",
        tagline="Five-rule fraud detection console",
        description="Forensic transaction monitor: round-numbers, "
                     "duplicates, off-hours, rapid-sequential, first-time. "
                     "AI writes the investigation note per flag.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["forensic", "audit", "fraud"],
        port=1023,
        accounting_focus="Internal audit and fraud detection",
        ai_integration="DeepSeek writes investigation notes",
    ),
    Project(
        day=24, folder="day-24-ddm-valuation",
        name="DDM.",
        tagline="Three-stage dividend discount model",
        description="High growth + transition + Gordon terminal. AI "
                     "interrogates each assumption against the dividend "
                     "history.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["valuation", "ddm", "dividends"],
        port=1024,
        accounting_focus="Equity valuation",
        ai_integration="DeepSeek writes the working-paper commentary",
    ),
    Project(
        day=25, folder="day-25-coa-generator",
        name="Ledger.",
        tagline="AI-generated chart of accounts",
        description="Describe a business in plain English; AI designs the "
                     "chart of accounts for entity type, industry, size and "
                     "standard. Validated against the 1000-9999 convention.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["bookkeeping", "coa", "system-design"],
        port=1025,
        accounting_focus="Accounting system design",
        ai_integration="DeepSeek designs the chart of accounts",
    ),
    Project(
        day=26, folder="day-26-equity-research",
        name="Equity.",
        tagline="One-page sell-side research note",
        description="Drop in five years of financials; AI writes the "
                     "rating, target price, investment thesis, bull and "
                     "bear cases, risks and catalysts.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["equity-research", "valuation", "ir"],
        port=1026,
        accounting_focus="Equity research methodology",
        ai_integration="DeepSeek drafts the research note",
    ),
    Project(
        day=27, folder="day-27-payroll-variance",
        name="Roll.",
        tagline="Payroll variance analyser",
        description="Classify every period-on-period variance into starters, "
                     "leavers, salary changes, overtime, bonus, NIC effects, "
                     "pension changes. AI narrates the period story.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["payroll", "people-cost", "reconciliation"],
        port=1027,
        accounting_focus="Payroll accounting",
        ai_integration="DeepSeek narrates the variance bridge",
    ),
    Project(
        day=28, folder="day-28-valuation-aggregator",
        name="Field.",
        tagline="Football-field valuation aggregator",
        description="Four valuation methods side by side (DCF, EV/EBITDA, "
                     "P/E, NAV) with AI weighting by sector and stage.",
        stack=["Python", "Flask", "matplotlib", "DeepSeek"],
        tags=["valuation", "football-field", "aggregator"],
        port=1028,
        accounting_focus="Investment banking valuation",
        ai_integration="DeepSeek weights methods + writes conclusion",
    ),
    Project(
        day=29, folder="day-29-accounting-chatbot",
        name="Ledger.AI",
        tagline="ACA-qualified accounting chatbot",
        description="UK accounting Q&A: IFRS / FRS 102 / IAS treatment, "
                     "journal entries with Dr / Cr lines, audit and tax. "
                     "Cites standards by name and number.",
        stack=["Python", "Flask", "openpyxl", "DeepSeek"],
        tags=["chatbot", "ifrs", "training"],
        port=1029,
        accounting_focus="Technical accounting reference",
        ai_integration="DeepSeek answers in voice of ACA accountant",
    ),
]
