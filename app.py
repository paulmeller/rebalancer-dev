import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


def get_price_data(tickers):
    # Use yfinance to get the price data for the given tickers
    data = yf.download(tickers, period="1d", interval="1d")["Close"]
    return data


def rebalance_portfolio(initial_weights, current_prices, target_weights, total_value):
    # Convert initial and target weights to numpy arrays
    initial_weights = np.array(initial_weights)
    target_weights = np.array(target_weights)

    # Calculate the current value of each asset in the portfolio
    current_values = current_prices * (total_value * initial_weights)

    # Calculate the target value of each asset in the portfolio
    target_values = total_value * target_weights

    # Calculate the difference between the current and target values for each asset
    value_diffs = target_values - current_values

    # Calculate the number of shares to buy or sell for each asset
    share_diffs = value_diffs / current_prices

    # Round the share differences to the nearest whole number
    share_diffs = np.round(share_diffs)

    # Calculate the final weights of each asset in the portfolio
    final_values = current_values + (share_diffs * current_prices)
    final_weights = final_values / (total_value)

    return final_weights


# Set the title and page layout
st.set_page_config(page_title='Portfolio Rebalancer', page_icon=':moneybag:')

# Define the sidebar
st.sidebar.title('Portfolio Rebalancer')

# Get user input for the stocks and their initial weights
st.sidebar.subheader('Initial Portfolio')
initial_weights = {}
stocks = []
for i in range(5):
    stock = st.sidebar.text_input(f'Stock {i + 1}', '').upper()
    if stock:
        stocks.append(stock)
        initial_weights[stock] = st.sidebar.number_input(f'{stock} Weight', min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# Get the current prices for the stocks using yfinance
current_prices = get_price_data(stocks)

# Get user input for the target weights of each stock in the portfolio
st.sidebar.subheader('Target Portfolio')
target_weights = {}
for stock in initial_weights.keys():
    target_weights[stock] = st.sidebar.number_input(f'{stock} Weight', min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# Get user input for the total value of the portfolio
st.sidebar.subheader('Total Portfolio Value')
total_value = st.sidebar.number_input('Total Value', min_value=0.0)

# Call the rebalance_portfolio function to get the final weights
final_weights = rebalance_portfolio(initial_weights.values(), current_prices, target_weights.values(), total_value)

# Display the final weights to the user
st.subheader('Final Portfolio')
weights_df = pd.DataFrame(final_weights, index=initial_weights.keys(), columns=['Weight'])
st.write(weights_df)
