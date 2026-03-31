"""
===========================================================
Create the client detail's page
===========================================================
Script purpose:
    Shows all details for a selected client including policy details,
    billing info, fund allocation, riders, and transaction history. 

"""

import streamlit as st
import pandas as pd
from utils.db_connection import connect_to_database
from utils.queries import get_policy, get_fund_info, get_riders, get_payments, update_policy, update_payment, add_payment, update_fund_info, add_policy, add_fund_info, add_rider, update_rider

if "selected_client_id" not in st.session_state:
    st.switch_page("pages/01_clients.py")

client_id = st.session_state["selected_client_id"]
client_name = st.session_state["selected_client_name"]

if st.button("← Back to Clients"):
    st.switch_page("pages/01_clients.py")

st.title(client_name)



policy = get_policy(client_id)
if policy is None:
    add_policy(client_id)
    st.rerun()

policy_id = policy[0]
fund_info = get_fund_info(policy_id)

if fund_info is None:
    add_fund_info(policy_id)
    st.rerun()

riders = get_riders(policy_id)
payments = get_payments(policy_id)



### SECTION 1: Plan Details
st.divider()
st.subheader("Plan Details")

col1, col2 = st.columns([4, 1])
with col1:
    st.write(f"**Plan Name:** {policy[2] or '—'}")
    st.write(f"**Policy Number:** {policy[3] or '—'}")
    st.write(f"**Issue Date:** {policy[4] or '—'}")
    st.write(f"**Face Amount:** ₱ {policy[5]:,.2f}" if policy[5] else "**Face Amount:** —")
    st.write(f"**Sum Assured:** ₱ {policy[6]:,.2f}" if policy[6] else "**Sum Assured:** —")
    st.write(f"**Policy Duration:** {policy[7] or '—'}")
    st.write(f"**Years to Pay:** {policy[8] or '—'}")
    st.write(f"**Remaining Years:** {policy[9] or '—'}")
with col2:
    if st.button("Edit", key="edit_plan"):
        st.session_state["editing_plan"] = True

if st.session_state.get("editing_plan"):
    with st.form("edit_plan_form"):
        st.subheader("Edit Plan Details")
        plan_name = st.text_input("Plan Name", value=policy[2] or "")
        policy_number = st.text_input("Policy Number", value=policy[3] or "")
        issue_date = st.date_input("Issue Date", value=policy[4] or None)
        face_amount = st.number_input("Face Amount", value=float(policy[5] or 0), format="%g")
        sum_assured = st.number_input("Sum Assured", value=float(policy[6] or 0), format="%g")
        policy_duration = st.text_input("Policy Duration", value=policy[7] or "")
        years_to_pay = st.number_input("Years to Pay", value=int(policy[8] or 0), step=1, format="%g")
        remaining_years = st.number_input("Remaining Years", value=float(policy[9] or 0), format="%g")
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")
        if save:
            update_policy(policy_id, (
                plan_name, policy_number, issue_date,
                face_amount, sum_assured, policy_duration,
                years_to_pay, remaining_years,
                policy[10], policy[11], policy[12],
                policy[13], policy[14]
            ))
            st.session_state["editing_plan"] = False
            st.success("Plan details updated!")
            st.rerun()
        if cancel:
            st.session_state["editing_plan"] = False
            st.rerun()



### SECTION 2: Status & Billing information
st.divider()
st.subheader("Status & Billing")

col1, col2 = st.columns([4, 1])
with col1:
    st.write(f"**Status:** {policy[10] or '—'}")
    st.write(f"**Premium Due:** {policy[11] or '—'}")
    st.write(f"**Mode of Payment:** {policy[12] or '—'}")
    st.write(f"**Premium Amount:** ₱ {policy[13]:,.2f}" if policy[13] else "**Premium Amount:** —")
    st.write(f"**Total Annual Premium:** ₱ {policy[14]:,.2f}" if policy[14] else "**Total Annual Premium:** —")
    total_paid = sum(p[4] for p in payments if p[7] == 'Paid') if payments else 0
    st.write(f"**Total Payments Made:** ₱ {total_paid:,.2f}")
with col2:
    if st.button("Edit", key="edit_billing"):
        st.session_state["editing_billing"] = True

if st.session_state.get("editing_billing"):
    with st.form("edit_billing_form"):
        st.subheader("Edit Status & Billing")
        status = st.text_input("Status", value=policy[10] or "")
        premium_due = st.date_input("Premium Due", value=policy[11] or None)
        mode_of_payment = st.selectbox("Mode of Payment", 
            ["Quarterly", "Monthly", "Semi-Annual", "Annual"],
            index=["Quarterly", "Monthly", "Semi-Annual", "Annual"].index(policy[12]) if policy[12] else 0)
        premium_amount = st.number_input("Premium Amount", value=float(policy[13] or 0), format="%g")
        total_annual_premium = st.number_input("Total Annual Premium", value=float(policy[14] or 0), format="%g")
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")
        if save:
            update_policy(policy_id, (
                policy[2], policy[3], policy[4],
                policy[5], policy[6], policy[7],
                policy[8], policy[9],
                status, premium_due, mode_of_payment,
                premium_amount, total_annual_premium
            ))
            st.session_state["editing_billing"] = False
            st.success("Billing info updated!")
            st.rerun()
        if cancel:
            st.session_state["editing_billing"] = False
            st.rerun()


### SECTION 3: Fund Allocation
st.divider()
st.subheader("Fund Allocation")

col1, col2 = st.columns([4, 1])
with col1:
    st.write(f"**Current Fund Value:** ₱ {fund_info[2]:,.2f}" if fund_info[2] else "**Current Fund Value:** —")
    st.write(f"**Fund Name:** {fund_info[3] or '—'}")
    st.write(f"**Fund Allocation:** {fund_info[4] or '—'}%")
    st.write(f"**Cost of Insurance:** ₱ {fund_info[5]:,.2f}" if fund_info[5] else "**Cost of Insurance:** —")
    st.write(f"**As of Date:** {fund_info[6] or '—'}")
with col2:
    if st.button("Edit", key="edit_fund"):
        st.session_state["editing_fund"] = True

if st.session_state.get("editing_fund"):
    with st.form("edit_fund_form"):
        st.subheader("Edit Fund Allocation")
        current_fund_value = st.number_input("Current Fund Value", value=float(fund_info[2] or 0), format="%g")
        fund_name = st.text_input("Fund Name", value=fund_info[3] or "")
        fund_allocation_pct = st.number_input("Fund Allocation %", value=float(fund_info[4] or 0), format="%g")
        cost_of_insurance = st.number_input("Cost of Insurance", value=float(fund_info[5] or 0), format="%g")
        as_of_date = st.date_input("As of Date", value=fund_info[6] or None)
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")
        if save:
            update_fund_info(fund_info[0], current_fund_value, fund_name, fund_allocation_pct, cost_of_insurance, as_of_date)
            st.session_state["editing_fund"] = False
            st.success("Fund info updated!")
            st.rerun()
        if cancel:
            st.session_state["editing_fund"] = False
            st.rerun()



### SECTION 4: Supplemental Benefits, Policy Rider
st.divider()
st.subheader("Supplemental Benefits")

if len(riders) == 0:
    st.info("No riders added yet.")
else:
    df_riders = pd.DataFrame(riders, columns=["ID", "Policy ID", "Rider Name", "Amount", "Active"])
    st.dataframe(df_riders[["Rider Name", "Amount", "Active"]], use_container_width=True)

with st.expander("Edit Rider"):
    if len(riders) == 0:
        st.info("No riders to edit yet.")
    else:
        rider_options = {f"{r[2]} - ₱{r[3]:,.2f}": r for r in riders}
        selected_label = st.selectbox("Select rider to edit", list(rider_options.keys()))
        selected_rider = rider_options[selected_label]

        with st.form("edit_rider_form"):
            rider_name = st.text_input("Rider Name", value=selected_rider[2] or "")
            rider_amount = st.number_input("Amount", value=float(selected_rider[3] or 0), format="%g")
            save = st.form_submit_button("Save Changes")
            if save:
                update_rider(selected_rider[0], rider_name, rider_amount)
                st.success("Rider updated")
                st.rerun()

with st.expander("Add New Rider"):
    with st.form("add_rider_form"):
        rider_name = st.text_input("Rider Name")
        rider_amount = st.number_input("Amount", min_value=0.0, format="%g")
        submitted = st.form_submit_button("Add Rider")
        if submitted:
            if rider_name.strip() == "":
                st.error("Please enter a rider name")
            else:
                add_rider(policy_id, rider_name, rider_amount)
                st.success("Rider added!")
                st.rerun()



### SECTION 5: Transaction HIstory
st.divider()
st.subheader("Transaction History")

if len(payments) == 0:
    st.info("No payments recorded yet.")
else:
    years = sorted(set(p[2] for p in payments))
    for year in years:
        year_payments = [p for p in payments if p[2] == year]
        year_total = sum(p[4] for p in year_payments if p[4])
        st.markdown(f"**Year {year}**")
        df_payments = pd.DataFrame(year_payments, 
            columns=["ID", "Policy ID", "Year", "Due Date", "Amount", "Date Paid", "Status", "Created At"])
        st.dataframe(df_payments[["Due Date", "Amount", "Date Paid", "Status"]], use_container_width=True)
        st.write(f"Year {year} Total: ₱ {year_total:,.2f}")
        st.write("")


with st.expander("Edit Payment"):
    if len(payments) > 0:
        payment_options = {f"Year {p[2]} - {p[3]} ({p[6]})": p for p in payments}
        selected_label = st.selectbox("Select payment to edit", list(payment_options.keys()))
        selected_payment = payment_options[selected_label]

        with st.form("edit_payment_form"):
            due_date = st.date_input("Due Date", value=selected_payment[3])
            amount = st.number_input("Amount", value=float(selected_payment[4] or 0), format="%g")
            date_paid = st.date_input("Date Paid", value=selected_payment[5] or None)
            status = st.selectbox("Status", ["Paid", "Missed", "DUE", "--"],
                index=["Paid", "Missed", "DUE", "--"].index(selected_payment[6]) if selected_payment[6] in ["Paid", "Missed", "DUE", "--"] else 0)
            save = st.form_submit_button("Save Changes")
            if save:
                update_payment(selected_payment[0], due_date, amount, date_paid, status)
                st.success("Payment updated!")
                st.rerun()

with st.expander("Add New Payment"):
    with st.form("add_payment_form"):
        year_number = st.number_input("Year Number", min_value=1, step=1, format="%g")
        due_date = st.date_input("Due Date")
        amount = st.number_input("Amount", min_value=0.0, format="%g")
        date_paid = st.date_input("Date Paid")
        status = st.selectbox("Status", ["Paid", "Missed", "DUE", "--"])
        submitted = st.form_submit_button("Add Payment")
        if submitted:
            add_payment(policy_id, year_number, due_date, amount, date_paid, status)
            st.success("Payment added!")
            st.rerun()
