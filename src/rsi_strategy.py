import pandas as pd
import pandas_ta as ta
import os

# load SPY data from csv
def load_data(ticker="SPY"):
    path = os.path.join("data", f"{ticker}.csv")

    # skip first 2 rows and set correct headers
    df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    
    df.index = pd.to_datetime(df.index)
    return df

# add RSI indicator to dataframe
def add_rsi(df, length=14):
    df["RSI"] = ta.rsi(df["Adj Close"], length=length)
    return df

# generate trading signals based on RSI thresholds
# 0 = no position, 1 = buy, -1 = sell
def generate_signals(df, lower=30, upper=70):
    df["Signal"] = 0
    df.loc[df["RSI"] < lower, "Signal"] = 1
    df.loc[df["RSI"] > upper, "Signal"] = -1
    return df
