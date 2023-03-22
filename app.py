import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title='Portfolio Rebalancing Tool')

st.title('Portfolio Rebalancing Tool')
st.write('Enter a list of stock tickers and their corresponding weightings, and select the rebalancing frequency.')

@st.cache_data
def get_data(ticker, start_date, end_date):
    df = yf.download(ticker, start_date, end_date)
    df['Ticker'] = ticker
    return df.reset_index().set_index(['Ticker', 'Date'])

def get_allocations(tickers_list, weights_list):
    num_tickers = len(tickers_list)
    allocations = pd.DataFrame({'Ticker': tickers_list, 'Weight': weights_list})
    allocations['Allocation'] = allocations['Weight'] / allocations['Weight'].sum()
    return allocations.set_index('Ticker')

st.sidebar.set_option('deprecation.showPyplotGlobalUse', False)

tickers_weights = st.sidebar.text_input('Enter comma-separated list of stock tickers and their corresponding weightings (e.g. AAPL:0.5,GOOG:0.3,MSFT:0.2):')
if st.sidebar.button('Submit'):
    tickers_weights_list = [tw.split(':') for tw in tickers_weights.upper().split(',') if tw.strip()]
    tickers_list = [tw[0] for tw in tickers_weights_list]
    weights_list = [float(tw[1]) for tw in tickers_weights_list]
    st.write('Tickers:', tickers_list)
    st.write('Weights:', weights_list)

    start_date = '2020-01-01'
    end_date = '2023-03-22'

    data = pd.concat([get_data(t, start_date, end_date) for t in tickers_list], axis=0)
    st.write('Data:', data)

    # Sidebar
    st.sidebar.subheader('Rebalancing Settings')

    # Rebalancing Frequency
    rebalance_freq = st.sidebar.selectbox('Rebalancing Frequency', ['Monthly', 'Quarterly', 'Yearly'])

    if sum(weights_list) != 1.0:
        st.error('Invalid weights input. Please enter a comma-separated list of weightings that add up to 1.0.')
    else:
        allocations = get_allocations(tickers_list, weights_list)
        st.write('Allocations:', allocations)
