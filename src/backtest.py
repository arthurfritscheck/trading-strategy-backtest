import os
import pandas as pd
from data_download import fetch_data
from rsi_strategy import add_rsi, generate_signals as generate_rsi_signals
from sma_strategy import add_sma, generate_signals as generate_sma_signals
from benchmark import simulate_buy_and_hold
from metrics import calculate_cagr, calculate_volatility, calculate_sharpe, calculate_max_drawdown
from plot import plot_signals, plot_portfolio_comparison

def simulate_trades(df, initial_cash=10000):
    """
    Simulates a trading strategy based on signals.
    """
    cash = initial_cash
    position = 0
    portfolio = []

    df = df.copy()
    #df = df.copy().iloc[1:]

    for i in range(len(df)):
        price = df["Adj Close"].iloc[i]
        signal = df["Signal"].iloc[i]

        if signal == 1 and position == 0:
            position = cash / price
            cash = 0
        elif signal == -1 and position > 0:
            cash = position * price
            position = 0

        total_value = cash + position * price
        portfolio.append(total_value)

    df["Portfolio"] = portfolio
    return df


# execute backtest
if __name__ == "__main__":
    df = fetch_data(tickers="SPY", start="2015-01-01", end="2025-01-01", auto_adjust=False)

    strategies = {}

    # buy and hold strategy
    df_bh = df.copy()
    # print(df_bh.head())
    df_bh = simulate_buy_and_hold(df_bh)
    strategies["Buy and Hold"] = df_bh["Portfolio"]

    # backtest rsi strategy    
    df_rsi = df.copy()
    df_rsi = add_rsi(df_rsi)
    df_rsi = generate_rsi_signals(df_rsi)
    df_rsi = simulate_trades(df_rsi)
    strategies["RSI Strategy"] = df_rsi["Portfolio"]

    plot_signals(df_rsi, indicator_col="RSI", strategy_name="RSI Strategy")

    # sma strategy
    df_sma = df.copy()
    df_sma = add_sma(df_sma)
    df_sma = generate_sma_signals(df_sma)
    df_sma = simulate_trades(df_sma)
    strategies["SMA Crossover"] = df_sma["Portfolio"]

    plot_signals(df_sma, indicator_col="SMA50", strategy_name="SMA Crossover")

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # print risk metrics 
    for strategy_name, portfolio in strategies.items():
        print(f"\n--- {strategy_name} Metrics ---")
        cagr = calculate_cagr(portfolio)
        vol = calculate_volatility(portfolio)
        sharpe = calculate_sharpe(portfolio)
        mdd = calculate_max_drawdown(portfolio)

        print(f"CAGR: {cagr:.2%}")
        print(f"Volatility: {vol:.2%}")
        print(f"Sharpe Ratio: {sharpe:.2f}")
        print(f"Max Drawdown: {mdd:.2%}")

        filename = strategy_name.lower().replace(" ", "_") + ".csv"
        output_path = os.path.join(output_dir, filename)
        
        save_df = pd.DataFrame({
            "Adj Close": df["Adj Close"],
            "Portfolio": portfolio
        })

        save_df.to_csv(output_path)
        print(f"Backtest for {strategy_name} complete. Results saved to {output_path}")
    

    plot_portfolio_comparison(strategies, df)