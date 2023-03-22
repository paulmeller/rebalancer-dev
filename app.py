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
def rebalance_portfolio(portfolio):
    prices = {}
    for stock in portfolio.keys():
        ticker = yf.Ticker(stock)
        prices[stock] = ticker.history(period='1d')['Close'][0]
    total_value = calculate_portfolio_value(portfolio, prices)
    if total_value > 100000:
        for stock, weight in portfolio.items():
            portfolio[stock] = weight * (100000 / total_value)
    return portfolio

# Define the initial portfolio weights
portfolio = {'GOOG': 0.6, 'MSFT': 0.4}

# Rebalance the portfolio to a value of $100,000
portfolio = rebalance_portfolio(portfolio)

# Create a new dataframe with the portfolio holdings and current values
holdings = []
for stock, weight in portfolio.items():
    ticker = yf.Ticker(stock)
    price = ticker.history(period='1d')['Close'][0]
    value = weight * 100000
    holdings.append([stock, weight, price, value])
df_holdings = pd.DataFrame(holdings, columns=['Stock', 'Weight', 'Price', 'Value'])

# Display the portfolio holdings in a table
st.write(df_holdings)
