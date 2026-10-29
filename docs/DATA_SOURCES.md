# Data source inventory

| Dataset | Candidate | Status | Notes |
|---|---|---|---|
| NVDA minute OHLCV | Alpaca historical stock bars | Not connected | Requires API key and secret; feed coverage/entitlements must be verified. |
| NVDA bid/ask quotes | Alpaca historical quotes | Not connected | Needed for realistic spread and slippage modeling. |
| QQQ minute OHLCV | Alpaca historical stock bars | Not connected | US technology-sector control. |
| Nasdaq-100 futures (NQ/MNQ) | Databento or licensed CME vendor | Not connected | Continuous contract and roll handling required. |
| TSMC Taiwan, SK Hynix Korea, Tokyo Electron Japan | Licensed local-exchange provider | Not selected | Point-in-time exchange calendars, FX and publication timing. |
| ASML, European indices | Licensed exchange provider | Not selected | Confirm local session overlap and timestamps. |
| CPI, FOMC, earnings calendar | Official release calendars / licensed events | Not connected | Record event announcement timestamps. |

Do not use Yahoo daily candles as substitutes for executable minute bars. Never commit API keys or licensed raw datasets to this public repository.
