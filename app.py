import pandas as pd
import streamlit as st

st.title("Churn Discount ROI Simulator")

df = pd.read_csv("roi_customers.csv")

discount = st.slider("Discount on customer's bill (%)", 0, 50, 10)
reduction = st.slider("Share of churn risk the discount removes (%)", 0, 100, 30)
threshold = st.slider("Offer only to customers with churn chance above (%)", 0, 100, 30)

targets = df[df['churn_prob'] >= threshold / 100]

# Savings: churn risk removed, valued at each customer's CLV
savings = (targets['churn_prob'] * reduction / 100 * targets['clv']).sum()
# Cost: the discount, applied to the value of the customer's remaining bills
cost = (discount / 100 * targets['clv']).sum()
net = savings - cost

col1, col2, col3 = st.columns(3)
col1.metric("Customers targeted", f"{len(targets):,}")
col2.metric("Expected savings", f"${savings:,.0f}")
col3.metric("Discount cost", f"${cost:,.0f}")

st.metric("Net gain", f"${net:,.0f}")
if net > 0:
    st.success("This offer pays for itself under these assumptions.")
else:
    st.error("This offer costs more than it saves under these assumptions.")
