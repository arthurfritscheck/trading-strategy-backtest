import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")


def load_backtest(filepath):
    df = pd.read_csv(filepath, index_col="Date", parse_dates=True)
    return df


def plot_portfolio_comparison(strategies, df, output_dir="output"):
    plt.figure(figsize=(12, 6))

    for name, portfolio in strategies.items():
        plt.plot(df.index, portfolio, label=name)

    plt.title("Portfolio Value Comparison")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "portfolio_comparison.png")
    plt.savefig(path)
    print(f"Portfolio comparison saved to {path}")
    plt.show()


# signal plotter
def plot_signals(df, indicator_col, strategy_name, output_dir="output"):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[indicator_col], label=indicator_col, color="purple")

    # horizontal lines if this is RSI-style logic
    if indicator_col.upper() == "RSI":
        plt.axhline(70, color="red", linestyle="--", label="Overbought (70)")
        plt.axhline(30, color="green", linestyle="--", label="Oversold (30)")

    buy = df[df["Signal"] == 1]
    sell = df[df["Signal"] == -1]

    plt.scatter(buy.index, buy[indicator_col], marker="^", color="green", label="Buy", s=100)
    plt.scatter(sell.index, sell[indicator_col], marker="v", color="red", label="Sell", s=100)

    plt.title(f"{strategy_name} - Buy/Sell Signals on {indicator_col}")
    plt.xlabel("Date")
    plt.ylabel(indicator_col)
    plt.legend()
    plt.tight_layout()

    filename = strategy_name.lower().replace(" ", "_") + f"_{indicator_col.lower()}_signals.png"
    path = os.path.join(output_dir, filename)
    plt.savefig(path)
    print(f"{strategy_name} signal plot saved to {path}")
    plt.show()
