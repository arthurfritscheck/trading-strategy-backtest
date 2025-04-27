from metrics import calculate_cagr, calculate_volatility, calculate_sharpe, calculate_max_drawdown
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

# simulate trades and track portfolio value over time starting with fixed cash amount
# all-in on buy and all-out on sell are assumed
def simulate_trades(df, initial_cash=10000):
    position = 0
    cash = initial_cash
    portfolio = []

    for i in range(1, len(df)):
        price = df["Adj Close"].iloc[i]
        signal = df["Signal"].iloc[i]

        # Buy if RSI is low and no current position
        if signal == 1 and position == 0:
            position = cash / price
            cash = 0
        
        # Sell if RSI is high and currently holding a position
        elif signal == -1 and position > 0:
            cash = position * price
            position = 0

        # portfolio value
        total = cash + position * price
        portfolio.append(total)

    df = df.iloc[1:].copy()
    df["Portfolio"] = portfolio
    return df

# execute backtest
if __name__ == "__main__":
    df = load_data("SPY")
    df = add_rsi(df)
    df = generate_signals(df)
    df = simulate_trades(df)
    
    # print risk metrics
    cagr = calculate_cagr(df)
    vol = calculate_volatility(df)
    sharpe = calculate_sharpe(df)
    mdd = calculate_max_drawdown(df)

    print(f"CAGR: {cagr:.2%}")
    print(f"Volatility: {vol:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {mdd:.2%}")

    output_path = os.path.join("output", "SPY_rsi_backtest.csv")
    df.to_csv("output/SPY_rsi_backtest.csv") # save results to output folder
    print(f"Backtest complete. Results saved to {output_path}")
