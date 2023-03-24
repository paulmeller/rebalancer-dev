import yfinance as yf
import streamlit as st

# Define function to get stock data and calculate trades
def rebalance_portfolio(portfolio):
    # Get stock data from yfinance
    data = yf.download(portfolio.keys())
    # Calculate current portfolio value
    current_value = (data['Adj Close'] * portfolio.values()).sum()
    # Calculate target portfolio value
    target_value = current_value.sum()
    target_weights = current_value / target_value
    # Calculate trades required to rebalance portfolio
    trades = target_weights - portfolio.values()
    trades *= target_value / data['Adj Close'].iloc[-1]
    trades = trades.round(0).astype(int)
    # Create summary table of trades
    summary = pd.DataFrame({'Ticker': portfolio.index, 'Target Weight': target_weights, 'Current Weight': portfolio.values(), 'Shares': trades})
    summary = summary[summary['Shares'] != 0]
    return summary

# Define function to display summary table
def display_summary(summary):
    st.write('## Summary of Trades')
    st.write(summary)

# Define main function
def main():
    # Set page title
    st.set_page_config(page_title='Portfolio Rebalancer')
    # Set page header
    st.write('# Portfolio Rebalancer')
    # Get user input for portfolio
    st.write('## Input Portfolio')
    tickers = st.text_input('Enter ticker symbols separated by commas (e.g., AAPL, GOOG)', 'AAPL,GOOG')
    weights = st.text_input('Enter target weights separated by commas (e.g., 0.5, 0.5)', '0.5,0.5')
    tickers = [ticker.strip().upper() for ticker in tickers.split(',')]
    weights = [float(weight.strip()) for weight in weights.split(',')]
    portfolio = pd.Series(index=tickers, data=weights)
    # Rebalance portfolio and display summary table
    summary = rebalance_portfolio(portfolio)
    display_summary(summary)

# Call main function
if __name__ == '__main__':
    main()
