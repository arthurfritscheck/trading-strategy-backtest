import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

# Load backtest results
def load_backtest(ticker="SPY"):
    path = os.path.join("output", f"{ticker}_rsi_backtest.csv")
    df = pd.read_csv(path, index_col="Date", parse_dates=True)
    return df

# Plot portfolio value over time
def plot_portfolio(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Portfolio"], label="Strategy Portfolio", color="navy")
    plt.title("Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/portfolio_value.png")
    plt.show()

# Plot RSI with buy/sell signals
def plot_rsi_signals(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["RSI"], label="RSI", color="purple")
    plt.axhline(70, color="red", linestyle="--", label="Overbought (70)")
    plt.axhline(30, color="green", linestyle="--", label="Oversold (30)")

    buy_signals = df[df["Signal"] == 1]
    sell_signals = df[df["Signal"] == -1]
    plt.scatter(buy_signals.index, buy_signals["RSI"], color="green", label="Buy", marker="^", s=100)
    plt.scatter(sell_signals.index, sell_signals["RSI"], color="red", label="Sell", marker="v", s=100)

    plt.title("RSI with Buy/Sell Signals")
    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/rsi_signals.png")
    plt.show()

# Main execution
if __name__ == "__main__":
    df = load_backtest("SPY")
    plot_portfolio(df)
    plot_rsi_signals(df)
