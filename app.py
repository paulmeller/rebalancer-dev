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
    for stock in portfolio.index:
        ticker = yf.Ticker(stock)
        prices[stock] = ticker.history(period='1d')['Close'][0]
    total_value = calculate_portfolio_value(portfolio.to_dict()['Weight'], prices)
    if total_value > target_value:
        for stock in portfolio.index:
            portfolio.loc[stock, 'Weight'] *= (target_value / total_value)
    shares = {}
    for stock in portfolio.index:
        shares[stock] = int(portfolio.loc[stock, 'Weight'] * target_value / prices[stock])
    return portfolio, shares, prices

# Define the initial portfolio weights as a dataframe
weights = pd.DataFrame({'Stock': ['GOOG', 'MSFT'], 'Weight': [0.6, 0.4]}).set_index('Stock')

# Rebalance the portfolio to a value of $100,000
portfolio, shares, prices = rebalance_portfolio(weights, 100000)

# Create a new dataframe with the portfolio holdings and current values
holdings = []
for stock in portfolio.index:
    weight = portfolio.loc[stock, 'Weight']
    ticker = yf.Ticker(stock)
    price = prices[stock]
    value = weight * 100000
    num_shares = shares[stock]
    holdings.append([stock, weight, price, value, num_shares, num_shares * price])
df_holdings = pd.DataFrame(holdings, columns=['Stock', 'Weight', 'Price', 'Value', 'Shares', 'On Hand'])

# Display the portfolio holdings in a table
st.write(df_holdings)
