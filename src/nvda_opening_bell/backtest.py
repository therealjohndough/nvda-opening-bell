"""Conservative bar-based research prototype. Not suitable for live trading."""
import argparse
from pathlib import Path
import pandas as pd


def backtest(frame: pd.DataFrame, capital: float = 1000.0, slippage_bps: float = 5.0):
    required = {"t", "o", "h", "l", "c", "v"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns: {required - set(frame.columns)}")
    df = frame.copy()
    df["t"] = pd.to_datetime(df["t"], utc=True).dt.tz_convert("America/New_York")
    df = df.sort_values("t")
    df["day"] = df["t"].dt.date
    trades = []
    equity = capital
    for day, group in df.groupby("day"):
        regular = group[(group["t"].dt.hour == 9) & (group["t"].dt.minute >= 30) |
                        ((group["t"].dt.hour == 9) & (group["t"].dt.minute < 50))]
        regular = regular[(regular["t"].dt.hour == 9) & regular["t"].dt.minute.between(30, 49)].copy()
        if len(regular) != 20 or list(regular["t"].dt.minute) != list(range(30, 50)):
            continue
        opening = regular.iloc[:5]
        high = opening["h"].max()
        regular["vwap"] = ((regular["h"] + regular["l"] + regular["c"]) / 3 * regular["v"]).cumsum() / regular["v"].cumsum()
        # Signal at a completed minute; entry at next minute open.
        for i in range(5, 15):
            bar = regular.iloc[i]
            if bar["c"] <= high or bar["c"] <= bar["vwap"]:
                continue
            next_bar = regular.iloc[i + 1]
            entry = float(next_bar["o"]) * (1 + slippage_bps / 10000)
            stop = float(opening["l"].min())
            if entry <= stop:
                continue
            risk_budget = equity * 0.0025
            shares = int(min(equity * 0.25 // entry, risk_budget // (entry - stop)))
            if shares < 1:
                continue
            # No intrabar stop modeling without quotes: conservative low-touch fill.
            exit_price = float(regular.iloc[-1]["c"]) * (1 - slippage_bps / 10000)
            reason = "time"
            for _, future in regular.iloc[i + 1:].iterrows():
                if float(future["l"]) <= stop:
                    exit_price = min(stop, float(future["o"])) * (1 - slippage_bps / 10000)
                    reason = "stop"
                    break
            pnl = shares * (exit_price - entry)
            equity += pnl
            trades.append({"day": str(day), "signal_time": str(bar["t"]),
                           "entry": entry, "exit": exit_price, "shares": shares,
                           "pnl": pnl, "equity": equity, "exit_reason": reason})
            break
    return pd.DataFrame(trades)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--capital", type=float, default=1000.0)
    parser.add_argument("--slippage-bps", type=float, default=5.0)
    parser.add_argument("--output", default="data/processed/trades.csv")
    args = parser.parse_args()
    trades = backtest(pd.read_csv(args.input), args.capital, args.slippage_bps)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    trades.to_csv(out, index=False)
    print(f"Trades: {len(trades)}")
    print(f"Net P&L: {trades['pnl'].sum():.2f}" if len(trades) else "No trades; check data coverage and sizing.")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
