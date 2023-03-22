import streamlit as st
import pandas as pd
import numpy as np

def rebalance_portfolio(initial_weights, current_prices, target_weights, total_value):
    # Convert initial and target weights to numpy arrays
    initial_weights = np.array(initial_weights)
    target_weights = np.array(target_weights)
    
    # Convert current prices to numpy array
    current_prices = np.array(list(current_prices.values()))

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

# Get user input for the initial weights of each asset in the portfolio
st.sidebar.subheader('Initial Weights')
initial_weights = {}
for asset in initial_weights.keys():
    initial_weights[asset] = st.sidebar.number_input(f'{asset} Weight', min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# Get user input for the current prices of each asset in the portfolio
st.sidebar.subheader('Current Prices')
prices = {}
for asset in initial_weights.keys():
    prices[asset] = st.sidebar.number_input(f'{asset} Price', min_value=0.0)

# Get user input for the target weights of each asset in the portfolio
st.sidebar.subheader('Target Weights')
target_weights = {}
for asset in initial_weights.keys():
    target_weights[asset] = st.sidebar.number_input(f'{asset} Weight', min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# Get user input for the total value of the portfolio
st.sidebar.subheader('Total Portfolio Value')
total_value = st.sidebar.number_input('Total Value', min_value=0.0)

# Call the rebalance_portfolio function to get the final weights
final_weights = rebalance_portfolio(initial_weights, prices, target_weights, total_value)

# Display the final weights to the user
st.subheader('Final Weights')
weights_df = pd.DataFrame(final_weights, index=prices.keys(), columns=['Weight'])
st.write(weights_df)
