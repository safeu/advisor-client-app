"""
===========================================================
Create the main page of the app
===========================================================
Script purpose:
    This script's purpose is to create the main page for the app;
    includes the app title, description, and others.

"""

import streamlit as st
from utils.queries import total_clients, total_missed_payments, total_payments_due

st.title("Advisor - Client Interactive App")
st.write("Manage and track insurance client policies")

st.divider()

col1, col2, col3 = st.columns(3)

total = total_clients()
missed = total_missed_payments()
due = total_payments_due()

with col1:
    st.metric(label="Total Clients", value=total[0])

with col2:
    st.metric(label="Missed Payments", value=missed[0])

with col3:
    st.metric(label="Payments Due", value=due[0])

st.divider()
st.write("Select a client from the **Clients** page to view or edit their policy details.")