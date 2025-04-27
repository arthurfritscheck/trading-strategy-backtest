import yfinance as yf
import pandas as pd
import os

def fetch_data(tickers, start=None, end=None, **kwargs):
    """
    Downloads data using yfinance and cleans the output:
    - Flattens MultiIndex columns
    - Removes any column name leftovers
    """
    df = yf.download(tickers, start=start, end=end, **kwargs)
    
    # if MultiIndex, flatten it
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)  # keep Open/Close/etc.
    df.columns.name = None  # remove 'Price' or 'Ticker' names if any
    
    return df


if __name__ == "__main__":
    ticker = "SPY"
    df = fetch_data(ticker, start="2015-01-01", end="2025-01-01", auto_adjust=False)

    # Save it to the data folder
    path = os.path.join("data", f"{ticker}.csv")
    df.to_csv(path)
    print(f"Downloaded and saved: {path}")
