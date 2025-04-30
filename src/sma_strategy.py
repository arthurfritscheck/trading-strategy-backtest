import pandas as pd

def add_sma(df, short_window=50, long_window=200):
    """
    Adds SMA50 and SMA200 to the dataframe.
    """
    df["SMA50"] = df["Adj Close"].rolling(window=short_window).mean()
    df["SMA200"] = df["Adj Close"].rolling(window=long_window).mean()
    return df

def generate_signals(df):
    """
    Generates signals based on SMA crossover:
    - Buy (1) when SMA50 crosses above SMA200
    - Sell (-1) when SMA50 crosses below SMA200
    """
    df["Signal"] = 0
    df["Signal"] = df["SMA50"] > df["SMA200"]
    df["Signal"] = df["Signal"].astype(int).diff().fillna(0)
    return df
