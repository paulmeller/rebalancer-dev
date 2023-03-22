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
    # Calculate the current portfolio value based on the latest stock prices
    total_value = calculate_portfolio_value(portfolio.to_dict()['Weight'], prices)
    # If the current value is greater than the target value, reduce the weights proportionally
    if total_value > target_value:
        for stock in portfolio.index:
            portfolio.loc[stock, 'Weight'] *= (target_value / total_value)
    # Calculate the target number of shares to hold for each stock based on the target weights and prices
    shares = {}
    for stock in portfolio.index:
        shares[stock] = int(portfolio.loc[stock, 'Weight'] * target_value / prices[stock])
    return portfolio, shares, prices

# Define the initial portfolio weights as a dataframe
df_weights = pd.DataFrame({'Stock': ['GOOG', 'STIP'], 'Weight': [0.6, 0.4]}).set_index('Stock')

# Display the table for the user to input initial holdings
try:
    target_portfolio = st.experimental_data_editor(df_weights)
except:
    st.warning("Unable to display the data editor. Please input your holdings as a CSV file with columns 'Stock' and 'Shares'.")

df_initial_holdings = pd.DataFrame({'ticker': ['GOOG', 'STIP'], 'Shares': [12, 29]}).set_index('ticker')
st.experimental_data_editor(df_initial_holdings)

# Get the current stock prices from Yahoo Finance
prices = {}
for stock in initial_holdings.index:
    ticker = yf.Ticker(stock)
    prices[stock] = ticker.history(period='1d')['Close'][0]
# Calculate the current value of the portfolio based on the initial holdings
initial_holdings['Price'] = initial_holdings.index.map(prices)
initial_holdings['On Hand'] = initial_holdings['Shares'] * initial_holdings['Price']

# Get the target portfolio value
target_portfolio_value = initial_holdings['On Hand'].sum()

# Rebalance the portfolio to match the target value
portfolio_weights = df_weights.copy()
proposed_portfolio, proposed_shares, proposed_prices = rebalance_portfolio(portfolio_weights, target_portfolio_value)

# Create a new dataframe with the proposed portfolio holdings and current values
proposed_holdings = []
for stock in proposed_portfolio.index:
    ticker = yf.Ticker(stock)
    price = proposed_prices[stock]
    num_shares = proposed_shares[stock]
    proposed_holdings.append([stock, price, num_shares, num_shares * price])
df_proposed_holdings = pd.DataFrame(proposed_holdings, columns=['Stock', 'Price', 'Shares', 'On Hand'])
df_proposed_holdings['Weight'] = df_proposed_holdings['On Hand'] / target_portfolio_value

# Display the proposed portfolio holdings in a table
st.write("Proposed Portfolio Holdings:")
st.write(df_proposed_holdings)

# Compare the initial holdings with the proposed holdings to get the trade details
trade_details = []
for stock in initial_holdings.index:
    if stock in df_proposed_holdings['Stock'].values:
        initial_shares = initial_holdings.loc[stock, 'Shares']
        new_shares = df_proposed_holdings.loc[df_proposed_holdings['Stock'] == stock, 'Shares'].values[0]
        trade_shares = new_shares - initial_shares
        if trade_shares > 0:
            trade_details.append(f"Buy {trade_shares} shares of {stock}")
        elif trade_shares < 0:
            trade_details.append(f"Sell {-trade_shares} shares of {stock}")
    else:
        trade_details.append(f"Sell all shares of {stock}")
for stock in df_proposed_holdings['Stock'].values:
    if stock not in initial_holdings.index:
        trade_details.append(f"Buy all shares of {stock}")

# Display the trade details
st.write("Trade Details:")
for trade in trade_details:
    st.write(trade)