# Import required libraries
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate monthly mortgage payment
def calculate_mortgage_payment(principal, annual_interest_rate, term_years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    num_payments = term_years * 12
    monthly_payment = principal * (monthly_interest_rate * np.power(1 + monthly_interest_rate, num_payments)) / (np.power(1 + monthly_interest_rate, num_payments) - 1)
    return monthly_payment

# Function to generate mortgage payment breakdown pie chart
def create_payment_breakdown_chart(principal, interest_rate, mortgage_term):
    plt.figure(figsize=(6, 6))
    labels = ['Principal', 'Interest']
    sizes = [principal, (interest_rate * mortgage_term * principal / 100)]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Mortgage Payment Breakdown')
    return plt

# Function to generate remaining balance bar chart
def create_remaining_balance_chart(principal, interest_rate, mortgage_term):
    num_years = np.arange(1, mortgage_term + 1)
    remaining_balances = [principal * (1 - (np.power(1 + interest_rate / 100, i) - 1) / np.power(1 + interest_rate / 100, mortgage_term)) for i in num_years]

    plt.figure(figsize=(10, 6))
    plt.bar(num_years, remaining_balances)
    plt.xlabel('Year')
    plt.ylabel('Remaining Balance ($)')
    plt.title('Remaining Mortgage Balance Over Time')
    plt.xticks(num_years)
    return plt

# App title and description
st.title("Mortgage Calculator")
st.write("Estimate your monthly mortgage payment based on the loan amount, interest rate, and term.")

# User inputs
home_price = st.number_input("Home Price", value=250000, step=1000, format="%i")
down_payment = st.number_input("Down Payment", value=50000, step=1000, format="%i")
mortgage_term = st.slider("Mortgage Term (Years)", min_value=10, max_value=30, value=30, step=1)
interest_rate = st.slider("Interest Rate (%)", min_value=0.0, max_value=10.0, value=3.5, step=0.1)

# Calculate mortgage principal and monthly payment
principal = home_price - down_payment
monthly_payment = calculate_mortgage_payment(principal, interest_rate, mortgage_term)

# Display the results
st.write(f"Loan Amount: ${principal:,.2f}")
st.write(f"Monthly Mortgage Payment: ${monthly_payment:,.2f}")

# Create and display visualizations
st.pyplot(create_payment_breakdown_chart(principal, interest_rate, mortgage_term))
st.pyplot(create_remaining_balance_chart(principal, interest_rate, mortgage_term))
