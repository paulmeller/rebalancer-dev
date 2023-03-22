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
df = pd.DataFrame({'Stock': ['GOOG', 'MSFT'], 'Weight': [0.6, 0.4]}).set_index('Stock')

# Define the initial portfolio holdings as a dataframe
holdings_df = pd.DataFrame({'Stock': ['GOOG', 'MSFT'], 'Shares': [40, 64]}).set_index('Stock')
prices = {}
for stock in holdings_df.index:
    ticker = yf.Ticker(stock)
    prices[stock] = ticker.history(period='1d')['Close'][0]
holdings_df['Price'] = holdings_df.index.map(prices)
holdings_df['On Hand'] = holdings_df['Shares'] * holdings_df['Price']
st.write(holdings_df)
portfolio_value = holdings_df['On Hand'].sum()

# Get user input for portfolio value
# portfolio_value = 100000 # st.number_input('Enter the value of your portfolio:', value=100000, step=1000, min_value=0.0, max_value=float("inf"))

# Rebalance the portfolio to the user-defined value
weights = df.copy()
portfolio, shares, prices = rebalance_portfolio(weights, portfolio_value)

# Create a new dataframe with the portfolio holdings and current values
holdings = []
for stock in portfolio.index:
    ticker = yf.Ticker(stock)
    price = prices[stock]
    num_shares = shares[stock]
    holdings.append([stock, price, num_shares, num_shares * price])
df_holdings = pd.DataFrame(holdings, columns=['Stock', 'Price', 'Shares', 'On Hand'])
df_holdings['Weight'] = df_holdings['On Hand'] / portfolio_value

# Display the portfolio holdings in a table
st.write(df_holdings)
