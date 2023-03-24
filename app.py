import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from mortgagecalc import FixedMortgage

# Set page title and favicon
st.set_page_config(page_title="Mortgage Calculator", page_icon=":money_with_wings:")

# Define function to calculate mortgage payments and generate amortization schedule
def calculate_mortgage(loan_amount, interest_rate, loan_term, down_payment, frequency):
    principal = loan_amount - down_payment
    mortgage = FixedMortgage(principal, interest_rate, loan_term)
    if frequency == 'Monthly':
        payment = mortgage.monthly_payment()
        schedule = mortgage.amortization_schedule()
    elif frequency == 'Bi-Weekly':
        payment = mortgage.biweekly_payment()
        schedule = mortgage.biweekly_amortization_schedule()
    elif frequency == 'Weekly':
        payment = mortgage.weekly_payment()
        schedule = mortgage.weekly_amortization_schedule()
    return payment, schedule

# Define Streamlit app
def app():
    # Set app title and subtitle
    st.title("Mortgage Calculator")
    st.write("Calculate your monthly mortgage payments and generate an amortization schedule.")
    
    # Set up input fields
    loan_amount = st.number_input("Loan Amount ($)", min_value=0.0, format="%f")
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, format="%f", step=0.01)
    loan_term = st.number_input("Loan Term (years)", min_value=1, format="%d")
    down_payment = st.number_input("Down Payment ($)", min_value=0.0, format="%f")
    frequency = st.selectbox("Payment Frequency", ["Monthly", "Bi-Weekly", "Weekly"])
    
    # Calculate mortgage payment and display results
    if st.button("Calculate"):
        payment, schedule = calculate_mortgage(loan_amount, interest_rate, loan_term, down_payment, frequency)
        st.write("Monthly Payment: $", "{:.2f}".format(payment))
        st.write("Total Interest Paid: $", "{:.2f}".format(schedule['interest'].sum()))
        
        # Display amortization schedule
        st.write("Amortization Schedule:")
        st.write(schedule)
        
        # Create plot of payment schedule
        payment_df = pd.DataFrame({'Payment': schedule['payment'], 'Principal': schedule['principal'], 'Interest': schedule['interest'], 'Balance': schedule['balance'], 'Month': schedule['month']})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=payment_df['Month'], y=payment_df['Principal'], name='Principal'))
        fig.add_trace(go.Scatter(x=payment_df['Month'], y=payment_df['Interest'], name='Interest'))
        fig.add_trace(go.Scatter(x=payment_df['Month'], y=payment_df['Payment'], name='Payment'))
        fig.add_trace(go.Scatter(x=payment_df['Month'], y=payment_df['Balance'], name='Balance'))
        fig.update_layout(title='Payment Schedule', xaxis_title='Month', yaxis_title='Dollars')
        st.plotly_chart(fig)
        
        # Create plot of interest vs. principal payments
        interest_df = pd.DataFrame({'Interest': schedule['interest'], 'Principal': schedule['principal']})
        fig = px.scatter(interest_df, x='Interest', y='Principal')
        fig.update_layout(title='Interest vs. Principal Payments', xaxis_title='Interest', yaxis_title='Principal')
       
# Run Streamlit app
if __name__ == '__main__':
    app()