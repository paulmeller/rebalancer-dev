import yfinance as yf
import pandas as pd
import streamlit as st

# Initialize session-based array to store tickers and weights
session_state = st.session_state
if "portfolio_data" not in session_state:
    session_state.portfolio_data = []

# Create a form for user input
st.header("Portfolio Rebalancing Tool")
st.subheader("Enter your current portfolio and target weights for each holding:")

# Create input fields for ticker symbols and current/target weights
ticker = st.text_input("Enter ticker symbol")
current_weight = st.number_input("Enter current weight as a percentage (e.g. 30)", min_value=0, max_value=100, value=0)
target_weight = st.number_input("Enter target weight as a percentage (e.g. 33.33)", min_value=0, max_value=100, value=0)

# Add stock to session-based array when user clicks the "Add Stock" button
if st.button("Add Stock"):
    if ticker != "" and current_weight > 0 and target_weight > 0:
        session_state.portfolio_data.append({"Ticker": ticker.upper(), "Current Weight": current_weight/100, "Target Weight": target_weight/100})
    else:
        st.warning("Please enter valid inputs for all fields.")

# Convert session-based array to pandas DataFrame
if len(session_state.portfolio_data) > 0:
    df = pd.DataFrame(session_state.portfolio_data)
    
    # Use yfinance to get pricing data for each holding
    try:
        prices = []
        for ticker in df["Ticker"]:
            prices.append(yf.Ticker(ticker).info["regularMarketPrice"])
        df["Price"] = prices
    except:
        st.error("Error: Failed to retrieve pricing data for one or more tickers.")
        st.stop()

    # Calculate the trades required to rebalance the portfolio
    try:
        total_value = sum([df["Current Weight"][i] * df["Price"][i] for i in range(len(df))])
        target_value = sum([df["Target Weight"][i] * df["Price"][i] for i in range(len(df))])
        df["Target Shares"] = [int(target_value*df["Target Weight"][i]/df["Price"][i]) for i in range(len(df))]
        df["Trade Shares"] = df["Target Shares"] - [int(total_value*df["Current Weight"][i]/df["Price"][i]) for i in range(len(df))]
        df["Trade Cost"] = df["Trade Shares"] * df["Price"]
    except:
        st.error("Error: Failed to calculate trades required to rebalance portfolio.")
        st.stop()

    # Display the summary of trades
    st.subheader("Summary of Trades Required to Rebalance Portfolio")
    st.write(df[["Ticker", "Trade Shares", "Trade Cost"]])

    # Display the DataFrame and allow the user to delete stocks from the session-based array
    st.subheader("Portfolio Data")
    delete_index = st.empty()
    delete_index_values = delete_index.multiselect("Select stocks to remove from portfolio", df.index.tolist())
    if delete_index_values:
        session_state.portfolio_data = df.drop(delete_index_values).to_dict("records")
        df = pd.DataFrame(session_state.portfolio_data)
        st.experimental_rerun()

    st.write(df)
else:
    st.warning("Please enter at least one stock to begin.")
