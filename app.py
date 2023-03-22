import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Define the function to calculate the portfolio value
def calculate_portfolio_value(portfolio, prices):
    total_value = 0
    for stock, weight in portfolio.items():
        total_value += prices[stock] * weight
    return total_value

# Define the function to rebalance the portfolio
@st.cache_data
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

# Define a function to display an editable table
def display_editable_table(df, title):
    st.write(f"### {title}")
    table = st.table(df)
    if table.add_rows or table.add_columns or table.delete_rows or table.delete_columns:
        df = pd.DataFrame(table.data, columns=table.columns)
    return df

# Define a function to plot the portfolio allocation
def plot_allocation(portfolio, prices):
    portfolio_values = {stock: prices[stock] * weight for stock, weight in portfolio.items()}
    fig = px.pie(names=list(portfolio.keys()), values=list(portfolio_values.values()))
    st.plotly_chart(fig)

# Display the table for the user to input initial holdings
current_portfolio = pd.DataFrame({'Ticker': ['AAPL', 'MSFT', 'GOOG'], 'Shares': [300, 500, 200]}).set_index('Ticker')
current_holdings = []
for stock in current_portfolio.index:
    price = 1 # proposed_prices[stock]
    num_shares = 1 # proposed_shares[stock]
    current_holdings.append([stock, price, num_shares, num_shares * price, current_portfolio.loc[stock, 'Shares']])


df_current_portfolio = pd.DataFrame({'Ticker': ['AAPL', 'MSFT', 'GOOG'], 'Shares': [300, 500, 200]}).set_index('Ticker')
# df_holdings = display_editable_table(df_current_holdings, 'Target Portfolio')
st.write(df_current_holdings)
df_holdings = df_current_holdings

# Get the current stock prices from Yahoo Finance
prices = {}
for stock in df_holdings.index:
    ticker = yf.Ticker(stock)
    prices[stock] = ticker.history(period='1d')['Close'][0]

# Calculate the current value of the portfolio based on the initial holdings
df_holdings['Price'] = df_holdings.index.map(prices)
df_holdings['Value'] = df_holdings['Price'] * df_holdings['Shares']
current_portfolio_value = df_holdings['Value'].sum()

# Define the initial portfolio weights as a dataframe
df_weights = pd.DataFrame({'Ticker': ['AAPL', 'MSFT', 'GOOG'], 'Weight': [0.3, 0.5, 0.2]}).set_index('Ticker')

# Ask the user for their target allocation
# df_target_weights = display_editable_table(df_weights, 'Target Weights')
df_target_weights = df_weights

# Calculate the target portfolio value
target_portfolio_value = current_portfolio_value * (df_target_weights['Weight'].sum() / df_weights['Weight'].sum())

# Rebalance the portfolio to match the target value
target_portfolio = df_target_weights.copy()
proposed_portfolio, proposed_shares, proposed_prices = rebalance_portfolio(target_portfolio, target_portfolio_value)

# Create a new dataframe with the proposed portfolio holdings and current values
proposed_holdings = []
for stock in proposed_portfolio.index:
    price = proposed_prices[stock]
    num_shares = proposed_shares[stock]
    proposed_holdings.append([stock, price, num_shares, num_shares * price, proposed_portfolio.loc[stock, 'Weight']])

df_proposed_holdings = pd.DataFrame(proposed_holdings, columns=['Stock', 'Price', 'Shares', 'Value', 'Weight'])

# Display the current and proposed portfolio allocations
st.write("### Portfolio Allocation")
st.write(f"Current value: ${current_portfolio_value:,.2f}")
plot_allocation(df_holdings['Shares'].to_dict(), prices)
proposed_portfolio_value = df_proposed_holdings['Value'].sum()
st.write(f"Proposed value: ${proposed_portfolio_value:,.2f}")
# plot_allocation(df_proposed_holdings['Shares'].to_dict(), proposed_prices)

# Display the proposed portfolio holdings in a table
st.write("### Proposed Portfolio Holdings")
st.write(df_proposed_holdings)

# Compare the initial holdings with the proposed holdings to get the trade details
trade_details = []
for stock in df_holdings.index:
    if stock in df_proposed_holdings['Stock'].values:
        initial_shares = df_holdings.loc[stock, 'Shares']
        new_shares = df_proposed_holdings.loc[df_proposed_holdings['Stock'] == stock, 'Shares'].values[0]
        trade_shares = new_shares - initial_shares
        if trade_shares > 0:
            trade_cost = trade_shares * proposed_prices[stock]
            trade_details.append(f"Buy {trade_shares} shares of {stock} for ${trade_cost:,.2f}")
        elif trade_shares < 0:
            trade_cost = -trade_shares * proposed_prices[stock]
            trade_details.append(f"Sell {-trade_shares} shares of {stock} for ${trade_cost:,.2f}")
    else:
        trade_details.append(f"Sell {df_holdings.loc[stock, 'Shares']} shares of {stock} for ${df_holdings.loc[stock, 'Value']:,.2f}")

for stock in df_proposed_holdings['Stock'].values:
    if stock not in df_holdings.index:
        new_shares = df_proposed_holdings.loc[df_proposed_holdings['Stock'] == stock, 'Shares'].values[0]
        trade_cost = new_shares * proposed_prices[stock]
        trade_details.append(f"Buy {new_shares} shares of {stock} for ${trade_cost:,.2f}")

# Display the trade details
if len(trade_details) > 0:
    st.write("### Trades Needed")
    for trade in trade_details:
        st.write(trade)
else:
    st.write("### No trades needed")
