import streamlit as st

# Define the tax brackets and rates for 2020
tax_brackets = [
    {'min_income': 0, 'max_income': 9875, 'rate': 0.10},
    {'min_income': 9876, 'max_income': 40125, 'rate': 0.12},
    {'min_income': 40126, 'max_income': 85525, 'rate': 0.22},
    {'min_income': 85526, 'max_income': 163300, 'rate': 0.24},
    {'min_income': 163301, 'max_income': 207350, 'rate': 0.32},
    {'min_income': 207351, 'max_income': 518400, 'rate': 0.35},
    {'min_income': 518401, 'max_income': float('inf'), 'rate': 0.37}
]

# Define the standard deduction and personal exemption amounts for 2020
standard_deduction = 12400
personal_exemption = 0

# Define the additional standard deduction amounts for certain taxpayers
additional_standard_deduction = {
    'single': 0,
    'married': 1300,
    'married_separate': 1300,
    'head_of_household': 1600
}

# Define the tax credit amounts for 2020
tax_credits = {
    'child_tax_credit': 2000,
    'earned_income_credit': 0
}

# Define the Streamlit app
def app():
    st.title("2020 US Tax Return Estimator")

    # Get user input for income and filing status
    income = st.number_input("Enter your income for 2020:")
    filing_status = st.selectbox(
        "Select your filing status:",
        ["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"]
    ).lower().replace(" ", "_")

    # Calculate the taxable income
    taxable_income = income - standard_deduction - additional_standard_deduction[filing_status] - personal_exemption
    if taxable_income < 0:
        taxable_income = 0

    # Calculate the income tax
    income_tax = 0
    for bracket in tax_brackets:
        if taxable_income > bracket['max_income']:
            income_tax += (bracket['max_income'] - bracket['min_income'] + 1) * bracket['rate']
        elif taxable_income > bracket['min_income']:
            income_tax += (taxable_income - bracket['min_income'] + 1) * bracket['rate']
            break

    # Calculate the total tax
    total_tax = income_tax

    # Calculate the tax due or refund
    withholding = st.number_input("Enter the total federal tax withholding for 2020:")
    estimated_tax_payments = st.number_input("Enter the total estimated tax payments for 2020:")
    refundable_credits = st.number_input("Enter the total refundable tax credits for 2020:")
    nonrefundable_credits = st.number_input("Enter the total non-refundable tax credits for 2020:")
    total_payments_and_credits = withholding + estimated_tax_payments + refundable_credits + nonrefundable_credits
    tax_due_or_refund = total_payments_and_credits - total_tax

    # Display the tax return estimate
    st.header("Tax Return Estimate")
    st.write(f"Taxable Income: ${taxable_income:,.2f}")
