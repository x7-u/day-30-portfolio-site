"""Day 30. Fun facts per project.

Each project page shows a couple of plain-English fun facts about what the
build actually does. These are curated, not generated, so the site is fully
static with no AI call at view time. If a folder is somehow missing from the
table below, a small deterministic fact is built from its metadata instead.

No em-dashes or en-dashes anywhere (plain ASCII hyphens only).
"""
from __future__ import annotations

FUN_FACTS: dict[str, list[str]] = {
    "day-01-ratio-dashboard": [
        "It reads a set of financial statements and grades them with red, amber and green flags, so the health of a business jumps out before you have read a single number.",
        "Day one of the run, and it already drafts its own management commentary in the voice of a financial controller.",
    ],
    "day-02-invoice-extractor": [
        "Drag in a stack of PDF invoices and it pulls out the line items, totals and supplier into one tidy ledger, with a confidence score on every row.",
        "Every extracted figure keeps an audit trail back to the invoice, so nothing is taken on trust.",
    ],
    "day-03-budget-tracker": [
        "It knows the difference between good and bad news: an overspend on costs is flagged red, but coming in under budget is celebrated, not punished.",
        "Each line can carry its own tolerance, so a lumpy travel budget is not held to the same standard as fixed rent.",
    ],
    "day-04-cashflow-model": [
        "Ask it 'what if revenue drops 20 percent for three weeks' in plain English and it rebuilds the whole 13-week cash forecast on the spot.",
        "The AI only reads the numbers and picks the scenario; the maths is done in plain Python, so the forecast always reconciles.",
    ],
    "day-05-sentiment-analyser": [
        "It reads a wall of financial news headlines and rolls the mood up from single companies to whole sectors.",
        "Extreme swings in sentiment get a traffic-light flag, so the signal stands out from the noise.",
    ],
    "day-06-breakeven-tool": [
        "It finds the exact point where a business stops losing money and starts making it, then runs thousands of simulations to show how likely you are to get there.",
        "Cost-volume-profit analysis with a Monte Carlo twist: the answer is a probability, not just a single number.",
    ],
    "day-07-earnings-summariser": [
        "Feed it an earnings call transcript and it fishes out the hedge phrases and forward-looking promises management would rather you skimmed past.",
        "Every claim it extracts comes with a confidence score.",
    ],
    "day-08-finance-categoriser": [
        "It sorts a bank statement into categories using a merchant dictionary first and only calls on AI for the genuinely odd ones, which keeps it fast and cheap.",
        "Built for the messy reality of real statements, not a tidy textbook example.",
    ],
    "day-09-dcf-model": [
        "A full five-year discounted cash flow valuation, with a 5 by 5 grid showing how the answer shifts as growth and the cost of capital change.",
        "A Monte Carlo overlay turns a single 'intrinsic value' into a realistic range.",
    ],
    "day-10-ap-ageing-report": [
        "It buckets every supplier invoice by how overdue it is (0-30, 30-60, 60-90, and 90 plus days) and points at the delays that look unusual.",
        "The kind of report a treasury team lives by, produced in seconds.",
    ],
    "day-11-sec-filing-parser": [
        "Point it at a company's SEC 10-K and it pulls out the risk section and the headline financials from a document that can run to hundreds of pages.",
        "It reads EDGAR filings so you do not have to.",
    ],
    "day-12-monte-carlo-sim": [
        "It runs ten thousand simulations of a multi-asset portfolio to map the full range of what could happen, not just the average.",
        "Returns, volatility and correlations are all yours to set.",
    ],
    "day-13-mgmt-accounts": [
        "Hand it a trial balance and it produces the three primary statements (profit and loss, balance sheet, and cash flow) with last year alongside.",
        "The monthly close, automated.",
    ],
    "day-14-jargon-explainer": [
        "Drop in any finance document and it builds a plain-English glossary of the jargon, so a board paper stops being a foreign language.",
        "Built to make finance readable for everyone, not only the specialists.",
    ],
    "day-15-inventory-optimiser": [
        "It works out exactly how much stock to order and when, balancing the cost of holding inventory against the cost of running out.",
        "Economic order quantity, the classic textbook formula, brought to life with real recommendations.",
    ],
    "day-16-ifrs16-calculator": [
        "It builds the full schedule IFRS 16 demands: the right-of-use asset, the lease liability, and the interest unwinding year by year.",
        "The standard that put leases on the balance sheet, handled end to end.",
    ],
    "day-17-tax-provision": [
        "A UK corporation tax computation, deferred tax and all, that also points out spend which might qualify for R&D relief.",
        "It works out the effective tax rate for you too.",
    ],
    "day-18-credit-scorecard": [
        "It scores a customer or supplier on the classic five factors of credit risk, then drafts the credit memo to go with the score.",
        "The decision and the write-up, in one pass.",
    ],
    "day-19-fx-exposure": [
        "It nets off your currency exposure by currency and time horizon, then suggests how much to hedge and with what.",
        "Treasury-desk thinking, made approachable.",
    ],
    "day-20-report-builder": [
        "It turns a profit-and-loss and a set of KPIs into a fully formatted Word document and Excel workbook, ready for the board pack.",
        "The fiddly formatting that eats an afternoon, done in moments.",
    ],
    "day-21-working-capital": [
        "It tracks how long cash is tied up in the business (days sales, days payable, days inventory, and the cash conversion cycle) against sector benchmarks.",
        "It is called 'Cycle.' because that is exactly what it measures: the cash cycle.",
    ],
    "day-22-wacc-calculator": [
        "It builds the weighted average cost of capital step by step and sanity-checks every input against what is normal for the sector.",
        "The single number that sits under every valuation, demystified.",
    ],
    "day-23-fraud-detection": [
        "Five forensic rules (round numbers, duplicates, off-hours, rapid-fire, and first-time payees) sweep a ledger for anything that smells off.",
        "Each flag arrives with a ready-drafted investigation note.",
    ],
    "day-24-ddm-valuation": [
        "A three-stage dividend discount model: fast growth, a transition, then a steady state, the way real dividend payers actually mature.",
        "It pressure-tests each assumption against the company's own dividend history.",
    ],
    "day-25-coa-generator": [
        "Describe a business in a sentence and it designs the whole chart of accounts for it, sized and structured for the industry.",
        "It keeps to the standard 1000 to 9999 numbering convention without being told.",
    ],
    "day-26-equity-research": [
        "It writes a one-page sell-side research note (rating, target price, the bull case and the bear case) from five years of financials.",
        "The sort of note that takes an analyst a day, drafted in a moment.",
    ],
    "day-27-payroll-variance": [
        "It explains why this month's payroll differs from last, splitting the change into starters, leavers, pay rises, overtime, bonuses and pension effects.",
        "It is called 'Roll.' and every penny of the movement is accounted for.",
    ],
    "day-28-valuation-aggregator": [
        "It lines up four ways of valuing a company side by side (DCF, multiples, P/E, and net assets) in the classic 'football field' chart bankers love.",
        "One picture, four opinions, a sensible conclusion.",
    ],
    "day-29-accounting-chatbot": [
        "Ask it a technical accounting question and it answers like a qualified accountant, citing the standard by name and number and showing the journal entries.",
        "Debits on the left, credits on the right, sources quoted.",
    ],
}


def fun_facts_for(summary) -> list[str]:
    """Return the curated fun facts for a project summary.

    ``summary`` is a ProjectSummary (it exposes ``.project``). Falls back to a
    small deterministic fact built from the project's own metadata if the
    folder is not in the curated table, so a page is never left blank."""
    project = getattr(summary, "project", summary)
    folder = getattr(project, "folder", "")
    facts = FUN_FACTS.get(folder)
    if facts:
        return list(facts)
    name = (getattr(project, "name", "") or "This project").replace(".", "").strip()
    stack = ", ".join(getattr(project, "stack", [])[:3]) or "Python and Flask"
    focus = (getattr(project, "accounting_focus", "") or "everyday finance").lower()
    return [
        f"{name} is a working build focused on {focus}.",
        f"It is put together with {stack}.",
    ]
