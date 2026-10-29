import pandas as pd
from src.nvda_opening_bell.backtest import backtest


def test_empty_data_rejected():
    try:
        backtest(pd.DataFrame())
    except ValueError:
        return
    raise AssertionError("Expected missing-column validation")


def test_missing_minute_session_is_skipped():
    bars = pd.DataFrame([{"t": "2026-10-01T13:30:00Z", "o": 100, "h": 101,
                          "l": 99, "c": 100, "v": 1000}])
    assert backtest(bars).empty
