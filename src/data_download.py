import yfinance as yf
import pandas as pd
import os


def fetch_data(ticker, start="2015-01-01", end="2025-01-01"):
    df = yf.download(ticker, start=start, end=end, progress=False)
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    ticker = "SPY"
    df = fetch_data(ticker)

    # Save it to the data folder
    path = os.path.join("data", f"{ticker}.csv")
    df.to_csv(path)
    print(f"Downloaded and saved: {path}")
