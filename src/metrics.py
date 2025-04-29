import numpy as np 

# CAGR (Compounded Annual Growth Rate)
def calculate_cagr(portfolio):
    start_value = portfolio.iloc[0]
    end_value = portfolio.iloc[-1]
    num_days = (portfolio.index[-1] - portfolio.index[0]).days
    num_years = num_days / 365.25
    cagr = (end_value / start_value) ** (1 / num_years) - 1
    return cagr

# Annualized volatility
def calculate_volatility(portfolio):
    daily_returns = portfolio.pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252)
    return volatility

# sharpe ratio
def calculate_sharpe(portfolio):
    daily_returns = portfolio.pct_change().dropna()
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    return sharpe

# max drawdown
def calculate_max_drawdown(portfolio):
    cum_max = portfolio.cummax()
    drawdown = portfolio / cum_max - 1
    max_drawdown = drawdown.min()
    return max_drawdown

