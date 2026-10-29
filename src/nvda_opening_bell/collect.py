"""Fetch historical minute bars from Alpaca's market data API. No order endpoints."""
import argparse
import os
from pathlib import Path
import requests
import pandas as pd


def fetch_bars(symbol: str, start: str, end: str, feed: str = "iex") -> pd.DataFrame:
    key = os.environ.get("ALPACA_API_KEY")
    secret = os.environ.get("ALPACA_API_SECRET")
    if not key or not secret:
        raise RuntimeError("Set ALPACA_API_KEY and ALPACA_API_SECRET (market data only).")
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars"
    params = {"start": start, "end": end, "timeframe": "1Min",
              "adjustment": "split", "feed": feed, "limit": 10000}
    rows = []
    while True:
        response = requests.get(url, params=params, headers={
            "APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        rows.extend(payload.get("bars", []))
        token = payload.get("next_page_token")
        if not token:
            break
        params["page_token"] = token
    frame = pd.DataFrame(rows)
    if not frame.empty:
        frame["t"] = pd.to_datetime(frame["t"], utc=True)
        frame = frame.sort_values("t").drop_duplicates("t")
    return frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", choices=["NVDA", "QQQ"], default="NVDA")
    parser.add_argument("--start", required=True, help="ISO date, inclusive")
    parser.add_argument("--end", required=True, help="ISO date, exclusive")
    parser.add_argument("--feed", default=os.environ.get("ALPACA_DATA_FEED", "iex"))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    frame = fetch_bars(args.symbol, args.start, args.end, args.feed)
    path = Path(args.output or f"data/raw/{args.symbol}_{args.start}_{args.end}.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    print(f"Wrote {len(frame)} rows to {path}")


if __name__ == "__main__":
    main()
