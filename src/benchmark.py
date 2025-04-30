def simulate_buy_and_hold(df, initial_cash=10000):
    """
    Simulate a simple buy-and-hold portfolio.
    Buy SPY at the first available Close price and never sell.
    """
    first_price = df["Adj Close"].iloc[1]
    shares_bought = initial_cash / first_price

    # Portfolio value over time
    df["Portfolio"] = shares_bought * df["Adj Close"]
    print(df.head())
    return df

