# NVDA Opening Bell — Research Lab

Research-only Python prototype for testing NVIDIA's first 20 minutes (09:30–09:50 ET). **No live trading or broker order submission is implemented.** The GitHub repository is public as of initial setup; never commit credentials or private account data.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ALPACA_API_KEY='your_key'
export ALPACA_API_SECRET='your_secret'
python -m src.nvda_opening_bell.collect --symbol NVDA --start 2026-08-30 --end 2026-10-29
python -m src.nvda_opening_bell.backtest --input data/raw/NVDA_2026-08-30_2026-10-29.csv
pytest -q
```

## Important limitations
- This is a baseline research prototype, **not a validated strategy**.
- Uses Alpaca IEX minute bars by default; incomplete exchange coverage may bias results.
- Uses minute OHLCV and simplified execution assumptions, not bid/ask quotes.
- No futures or foreign-market factors are integrated yet.
- The position sizing may produce zero trades for $500–$1,000 accounts because whole-share sizing is conservative.
- Stop handling is approximate; use quotes and event-driven execution simulation before trusting P&L.
- Never interpret a backtest as proof of future returns.

Read `docs/RESEARCH_PROTOCOL.md` and `docs/DATA_SOURCES.md` before extending.
