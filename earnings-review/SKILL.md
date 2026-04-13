---
name: earnings-review
description: "Post-earnings analysis reviewing beat/miss outcomes, new guidance, performance trajectory, and analyst commentary. Use when reviewing results after an earnings release."
disable-model-invocation: true
---
Review **$ARGUMENTS** after their earnings report.

Use the hedge-fund-analyst skill for domain judgment. If the user hasn't specified a data folder, ask for it.

## Beat/Miss Analysis

**Recent Quarter:**
- Did they beat or miss? By how much?
- Management's explanation for the variance

**Beat/Miss Table (last 4 quarters):**
| Metric | Q-4 | Q-3 | Q-2 | Q-1 (Most Recent) |
|--------|-----|-----|-----|-------------------|
| Revenue Estimate | | | | |
| Revenue Actual | | | | |
| Revenue Beat/Miss % | | | | |
| EPS Estimate | | | | |
| EPS Actual | | | | |
| EPS Beat/Miss % | | | | |

## Management Guidance Analysis

**New Guidance Provided (from most recent transcript/filings):**
- Revenue guidance: Range and midpoint for upcoming quarter/year
- EPS guidance: Range and midpoint
- Margin guidance: Gross/Operating/EBITDA targets
- Other KPI guidance: Specific metrics guided
- Forward-looking statements

**Guidance vs Expectations Table:**
| Metric | New Guidance | Prior Guidance | Consensus | vs Consensus |
|--------|--------------|----------------|-----------|--------------|
| Revenue | | | | Above/Below/In-line |
| EPS | | | | Above/Below/In-line |
| Margins | | | | Above/Below/In-line |

- Calculate implied growth rates from new guidance
- Compare new guidance trajectory vs same period last year (e.g., Q3 2026 guidance vs Q3 2025 actual)

**Management Commentary & Tone:**
- Review prior transcripts vs this transcript for tone changes
- Confidence levels when discussing key guidance metrics
- Key assumptions underlying guidance
- Risk factors or caveats mentioned
- Positive or negative tone shifts vs prior quarters

## Historical Performance & Growth Trajectory

**Build a table showing the last 8 quarters of actual results:**
| Metric | Q-8 | Q-7 | Q-6 | Q-5 | Q-4 | Q-3 | Q-2 | Q-1 |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|
| Revenue | | | | | | | | |
| Revenue YoY Growth % | | | | | | | | |
| Accelerating/Decelerating (bps QoQ) | | | | | | | | |
| EPS | | | | | | | | |
| EPS YoY Growth % | | | | | | | | |
| Accelerating/Decelerating (bps QoQ) | | | | | | | | |

Note if revenue growth is accelerating/decelerating (by how many basis points quarter-over-quarter).
Note if EPS growth is accelerating/decelerating (by how many basis points quarter-over-quarter).

**Growth Trajectory Assessment:**
- Which metrics are accelerating or decelerating over the last 8 quarters?
- Key drivers of these trends based on management commentary

## Street Q&A Analysis

**From the most recent transcript, create a table:**
| Analyst Question | Management Response | Well Answered (Y/N) |
|------------------|---------------------|---------------------|
| | | |
| | | |

Identify questions that weren't answered well or were deflected.

## Contradictions

Examine all documents for contradicting statements:
- Quote both conflicting statements with document source and page/section
- Explain why they're incompatible
- If none found, state explicitly: "No contradictions found."

Example format:
1. [Title of Document / Date]
   - Statement A: "Q3 revenue growth expected to be 15%" (Transcript, CEO remarks, p.2)
   - Statement B: "We are guiding for 8–10% revenue growth in Q3" (Earnings Report, p.10)
   - Explanation: These forecasts differ significantly, indicating inconsistent guidance.

## Executive Summary Structure

1. **Beat/Miss Context** (Revenue beat/miss, EPS beat/miss, key metrics)
2. **Management Guidance** (new guidance provided and comparison to expectations)
3. **Historical Performance** (YoY trends accelerating/decelerating with bps)
4. **Management Commentary** (highlight 1-2 key themes)
5. **Street Commentary** (highlight 1-2 key questions not answered well)
6. **Contradictions** (highlight 1-2 key contradictions if found)

**Output:** `{TICKER}_earnings_review.md`
