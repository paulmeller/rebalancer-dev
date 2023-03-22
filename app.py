import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title='Portfolio Rebalancing Tool')

st.title('Portfolio Rebalancing Tool')
st.write('Enter a list of stock tickers and select the rebalancing frequency and allocation.')

@st.cache_data
def get_data(ticker, start_date, end_date):
    df = yf.download(ticker, start_date, end_date)
    df['Ticker'] = ticker
    return df.reset_index().set_index(['Ticker', 'Date'])

st.sidebar.set_option('deprecation.showPyplotGlobalUse', False)

tickers = st.sidebar.text_input('Enter comma-separated list of stock tickers:')
if st.sidebar.button('Submit'):
    tickers_list = tickers.upper().split(',')
    st.write('Tickers:', tickers_list)

    start_date = '2020-01-01'
    end_date = '2023-03-22'

    data = pd.concat([get_data(t, start_date, end_date) for t in tickers_list], axis=0)
    st.write('Data:', data)

    # Sidebar
    st.sidebar.subheader('Rebalancing Settings')

    # Rebalancing Frequency
    rebalance_freq = st.sidebar.selectbox('Rebalancing Frequency', ['Monthly', 'Quarterly', 'Yearly'])

    # Allocation
    weights = st.sidebar.text_input('Enter comma-separated list of weights (e.g. 0.5,0.3,0.2):')
    weights_list = [float(w.strip()) for w in weights.split(',') if w.strip()]
    if not weights_list or sum(weights_list) != 1.0:
        st.error('Invalid weights input. Please enter a comma-separated list of weights that add up to 1.0.')
    else:
        allocations = get_allocations(tickers_list, weights_list)
        st.write('Allocations:', allocations)
