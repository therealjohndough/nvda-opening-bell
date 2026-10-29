# NVDA Opening Bell — Research Protocol v1

## Hypothesis
Overnight futures and foreign semiconductor-market returns provide incremental predictive information for NVDA's 9:35–9:50 ET tradable momentum beyond NVDA premarket information.

## Scope
- Last 60 calendar days for first retrospective, then 2+ years where licensed intraday data is available.
- US regular sessions only, America/New_York timezone.
- Long-only shares; at most one entry/day; no leverage; close by 09:50 ET.
- $500 and $1,000 account simulations, 0.25% equity risk per trade, 25% maximum notional exposure.
- No real-money execution. Paper execution is a future, separately reviewed milestone.

## Pre-register experiments
A: five-minute NVDA opening-range breakout, no overnight filters.
B: A with pre-09:30 Nasdaq-100 futures bias.
C: B with timestamp-correct Asian and European semiconductor factors.

Do not optimize parameters on evaluation data. Use walk-forward splits and a final untouched holdout. Report days with no trades and compare to a no-trade baseline. Include confidence intervals and transaction-cost sensitivity.

## Execution model
At 09:35 ET the opening range from 09:30 through 09:34 completed minute bars is known. A signal requires a completed subsequent minute bar close above the range high, above VWAP, adequate volume and spread filters. Enter no earlier than the next available bar (never on the signal bar's close without a realistic fill model). Exit on stop, target or time, whichever occurs first; ambiguous same-bar stop/target is resolved conservatively. No new positions after 09:45. Flat by 09:50, with failures escalated in future paper runner.

## Evaluation
Net P&L, win rate, trade count, expectancy, profit factor, maximum drawdown, slippage sensitivity, missed days, and error rates. Explicitly distinguish hypothesis from evidence.

## Data integrity
Use point-in-time values; document timezone, split adjustments, source coverage, session calendars, market holidays, missing bars, spreads, and event-day exclusions. No forward-filling missing execution prices.
