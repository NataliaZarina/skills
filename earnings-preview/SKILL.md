---
name: earnings-preview
description: "Pre-earnings analysis covering beat/miss history, management guidance patterns, consensus estimates, and a mini projection model. Use when the user wants to prepare for an upcoming earnings report or preview earnings."
disable-model-invocation: true
---
Analyze **$ARGUMENTS** before their upcoming earnings report.

Use the hedge-fund-analyst skill for domain judgment. If the user hasn't specified a data folder, ask for it.

## Beat/Miss Track Record

**Analysis:**
- Extract beat/miss history from `beat_miss_analysis` in financials JSON
- Calculate beat/miss percentage over last 12 quarters AND last 4 quarters separately
- Identify pattern: Consistent beater / Consistent misser / Mixed
- Track if beat magnitude is improving or deteriorating over time
- Include management's explanation for variance

**Beat/Miss Table Structure:**
| Metric | Q-4 | Q-3 | Q-2 | Q-1 (Most Recent) |
|--------|-----|-----|-----|-------------------|
| Revenue Estimate | | | | |
| Revenue Actual | | | | |
| Revenue Beat/Miss % | | | | |
| EPS Estimate | | | | |
| EPS Actual | | | | |
| EPS Beat/Miss % | | | | |

**Output:** `{TICKER}_past_earnings.md`

## Management Guidance Analysis

**Current Quarter Guidance:**
- Revenue guidance: Range and midpoint
- EPS guidance: Range and midpoint
- Margin guidance: Gross/Operating/EBITDA targets
- Other KPI guidance: Specific metrics guided

**Guidance Comparison:**
- Compare current Q guidance vs same quarter last year
- Calculate implied YoY growth rates
- Compare guidance vs consensus in a table
- Identify pattern: Conservative (guides low, beats) or Aggressive (guides high, misses)

**Management Commentary & Tone:**
- Confidence levels when discussing key guidance metrics
- Key assumptions underlying guidance
- Risk factors or caveats mentioned
- Positive or negative tone shifts vs prior quarters

**Post-Guidance Updates:**
- Any conferences or events since last earnings (from `news` section)
- Management commentary at industry events
- Relevant macro developments affecting guidance

**Output:** `{TICKER}_guidance_analysis.md`

## Consensus Estimates Analysis

**Build a table of historical & consensus metrics (8 quarters + next quarter projection):**
| Metric | Q-8 | Q-7 | Q-6 | Q-5 | Q-4 | Q-3 | Q-2 | Q-1 | Next Q |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|--------|
| Revenue Estimate | | | | | | | | | |
| Revenue YoY Growth % | | | | | | | | | |
| Acceleration (bps vs prior Q) | | | | | | | | | |
| EPS Estimate | | | | | | | | | |
| EPS YoY Growth % | | | | | | | | | |
| Acceleration (bps vs prior Q) | | | | | | | | | |
| FY Revenue Estimate | | | | | | | | | |
| FY EPS Estimate | | | | | | | | | |

Note if revenue/EPS growth is accelerating or decelerating by how many basis points.

**Output:** `{TICKER}_consensus_analysis.md`

## Mini Model

**Build a CSV with the following rows (8 quarters + next quarter projection):**
- Revenue
- Revenue Growth YoY %
- COGS
- Gross Profit
- Gross Margin %
- Basis Points change YoY in Gross Margin
- Opex (Gross Profit minus Operating Income)
- Opex Growth %
- Operating Income
- Taxes and Interest (Operating Income minus Net Income)
- Net Income
- Diluted Shares
- EPS (Net Income / Diluted Shares)

**Output:** `{TICKER}_model.csv`

## Executive Summary

**Structure:**
1. Earnings Date & Time (date, time, conference call details)
2. Consensus Expectations (Revenue, EPS, key metrics)
3. Beat/Miss History (track record and magnitude trend)
4. Management Guidance (current quarter targets and tone)
5. Growth Trajectory (YoY trends accelerating/decelerating with bps)
6. Contradictions (top 1-2 contradictions if found)
7. Mini Model (showing YoY growth rates)

**Output:** `{TICKER}_earnings_preview.md`
