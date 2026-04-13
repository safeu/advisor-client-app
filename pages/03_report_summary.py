"""
===========================================================
Client Report Summary Page
===========================================================
Script purpose:
    A clean, read-only summary of a client's policy details,
    designed to be downloaded as a PDF.
"""

import streamlit as st
import pandas as pd
from utils.queries import get_policy, get_fund_info, get_riders, get_payments
from utils.report_generator import generate_client_report

if not st.session_state.get("logged_in"):
    st.switch_page("main.py")

if "selected_client_id" not in st.session_state:
    st.switch_page("pages/01_clients.py")

client_id = st.session_state["selected_client_id"]
client_name = st.session_state["selected_client_name"]


policy = get_policy(client_id)
fund_info = get_fund_info(policy[0]) if policy else None
riders = get_riders(policy[0]) if policy else []
payments = get_payments(policy[0]) if policy else []

total_paid = sum(p[4] for p in payments if p[6] == 'Paid') if payments else 0

col1, col2 = st.columns(2)
with col1:
    if st.button("← Back to Client Detail"):
        st.switch_page("pages/02_client_detail.py")
with col2:
    pdf_bytes = generate_client_report(client_name, policy, fund_info, riders, payments)
    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_bytes,
        file_name=f"{client_name}_policy_summary.pdf",
        mime="application/pdf"
    )

st.title(f"Policy Summary — {client_name}")
st.write(f"**Total Payments Made:** ₱ {total_paid:,.2f}")
st.divider()


left, right = st.columns([1, 1])

with left:
    st.subheader("Plan Details")
    st.write(f"**Plan Name:** {policy[2] or '—'}")
    st.write(f"**Policy Number:** {policy[3] or '—'}")
    st.write(f"**Issue Date:** {policy[4] or '—'}")
    st.write(f"**Face Amount:** ₱ {policy[5]:,.2f}" if policy[5] else "**Face Amount:** —")
    st.write(f"**Sum Assured:** ₱ {policy[6]:,.2f}" if policy[6] else "**Sum Assured:** —")
    st.write(f"**Policy Duration:** {policy[7] or '—'}")
    st.write(f"**Years to Pay:** {policy[8] or '—'}")
    st.write(f"**Remaining Years:** {policy[9] or '—'}")

    st.divider()

    st.subheader("Status & Billing")
    st.write(f"**Status:** {policy[10] or '—'}")
    st.write(f"**Premium Due:** {policy[11] or '—'}")
    st.write(f"**Mode of Payment:** {policy[12] or '—'}")
    st.write(f"**Premium Amount:** ₱ {policy[13]:,.2f}" if policy[13] else "**Premium Amount:** —")
    st.write(f"**Total Annual Premium:** ₱ {policy[14]:,.2f}" if policy[14] else "**Total Annual Premium:** —")
    st.write(f"**Total Payments Made:** ₱ {total_paid:,.2f}")

    st.divider()

    st.subheader("Fund Allocation")
    if fund_info:
        st.write(f"**Current Fund Value:** ₱ {fund_info[2]:,.2f}" if fund_info[2] else "**Current Fund Value:** —")
        st.write(f"**Fund Name:** {fund_info[3] or '—'}")
        st.write(f"**Fund Allocation:** {fund_info[4] or '—'}%")
        st.write(f"**Cost of Insurance:** ₱ {fund_info[5]:,.2f}" if fund_info[5] else "**Cost of Insurance:** —")
        st.write(f"**As of Date:** {fund_info[6] or '—'}")

    st.divider()

    st.subheader("Supplemental Benefits")
    if len(riders) == 0:
        st.write("No riders.")
    else:
        df_riders = pd.DataFrame(riders, columns=["ID", "Policy ID", "Rider Name", "Amount", "Active"])
        st.dataframe(df_riders[["Rider Name", "Amount"]], use_container_width=True, hide_index=True)

with right:
    st.subheader("Transaction History")
    if len(payments) == 0:
        st.write("No payments recorded.")
    else:
        years = sorted(set(p[2] for p in payments))
        for year in years:
            year_payments = [p for p in payments if p[2] == year]
            year_total = sum(p[4] for p in year_payments if p[4])
            st.markdown(f"**Year {year}**")
            df_payments = pd.DataFrame(year_payments,
                columns=["ID", "Policy ID", "Year", "Due Date", "Amount", "Date Paid", "Status", "Created At"])
            st.dataframe(
                df_payments[["Due Date", "Amount", "Date Paid", "Status"]],
                use_container_width=True,
                hide_index=True
            )
            st.write(f"**Year {year} Total: ₱ {year_total:,.2f}**")
            st.write("")