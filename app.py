import streamlit as st
import pandas as pd
import yfinance as yf

# Define the function to calculate the portfolio value
def calculate_portfolio_value(portfolio, prices):
    total_value = 0
    for stock, weight in portfolio.items():
        total_value += prices[stock] * weight
    return total_value

# Define the function to rebalance the portfolio
def rebalance_portfolio(portfolio, target_value):
    prices = {}
    for stock in portfolio.keys():
        ticker = yf.Ticker(stock)
        prices[stock] = ticker.history(period='1d')['Close'][0]
    total_value = calculate_portfolio_value(portfolio, prices)
    if total_value > target_value:
        for stock, weight in portfolio.items():
            portfolio[stock] = weight * (target_value / total_value)
    shares = {}
    for stock, weight in portfolio.items():
        shares[stock] = int(weight * target_value / prices[stock])
    return portfolio, shares

# Define the initial portfolio weights
portfolio = {'GOOG': 0.6, 'MSFT': 0.4}

# Rebalance the portfolio to a value of $100,000
portfolio, shares = rebalance_portfolio(portfolio, 100000)

# Create a new dataframe with the portfolio holdings and current values
holdings = []
for stock, weight in portfolio.items():
    ticker = yf.Ticker(stock)
    price = ticker.history(period='1d')['Close'][0]
    value = weight * 100000
    num_shares = shares[stock]
    holdings.append([stock, weight, price, value, num_shares])
df_holdings = pd.DataFrame(holdings, columns=['Stock', 'Weight', 'Price', 'Value', 'Shares'])

# Display the portfolio holdings in a table
st.write(df_holdings)
