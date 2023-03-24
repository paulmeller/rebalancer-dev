import yfinance as yf
import pandas as pd
import streamlit as st

# Create a form for user input
st.header("Portfolio Rebalancing Tool")
st.subheader("Enter your current portfolio and target weights for each holding:")

# Create input fields for ticker symbols and current/target weights
tickers = st.text_input("Enter ticker symbols separated by commas (e.g. AAPL,MSFT,AMZN)", value="AAPL,MSFT,AMZN")
current_weights = st.text_input("Enter current weights as a percentage (e.g. 30,40,30)", value="30,40,30")
target_weights = st.text_input("Enter target weights as a percentage (e.g. 33.33,33.33,33.33)", value="33.33,33.33,33.33")

# Convert user input to pandas DataFrame
tickers_list = tickers.split(",")
current_weights_list = [float(x)/100 for x in current_weights.split(",")]
target_weights_list = [float(x)/100 for x in target_weights.split(",")]
data = {"Ticker": tickers_list, "Current Weight": current_weights_list, "Target Weight": target_weights_list}
df = pd.DataFrame(data)

# Use yfinance to get pricing data for each holding
prices = []
for ticker in tickers_list:
    prices.append(yf.Ticker(ticker).info["regularMarketPrice"])
df["Price"] = prices

# Calculate the trades required to rebalance the portfolio
total_value = sum([df["Current Weight"][i] * df["Price"][i] for i in range(len(df))])
target_value = sum([df["Target Weight"][i] * df["Price"][i] for i in range(len(df))])
df["Target Shares"] = [int(target_value*df["Target Weight"][i]/df["Price"][i]) for i in range(len(df))]
df["Trade Shares"] = df["Target Shares"] - [int(total_value*df["Current Weight"][i]/df["Price"][i]) for i in range(len(df))]
df["Trade Cost"] = df["Trade Shares"] * df["Price"]

# Display the summary of trades
st.subheader("Summary of Trades Required to Rebalance Portfolio")
st.write(df[["Ticker", "Trade Shares", "Trade Cost"]])
