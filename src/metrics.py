import numpy as np


# CAGR (Compounded Annual Growth Rate)
def calculate_cagr(df):
    start_value = df["Portfolio"].iloc[0]
    end_value = df["Portfolio"].iloc[-1]
    num_days = (df.index[-1] - df.index[0]).days
    num_years = num_days / 365.25
    cagr = (end_value / start_value) ** (1 / num_years) - 1
    return cagr

# annualized Volatility
def calculate_volatility(df):
    daily_returns = df["Portfolio"].pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252)
    return volatility

# sharpe Ratio (assume risk-free rate = 0)
def calculate_sharpe(df):
    daily_returns = df["Portfolio"].pct_change().dropna()
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    return sharpe

# max Drawdown (biggest % drop from peak)
def calculate_max_drawdown(df):
    cum_max = df["Portfolio"].cummax()
    drawdown = df["Portfolio"] / cum_max - 1
    max_drawdown = drawdown.min()
    return max_drawdown
