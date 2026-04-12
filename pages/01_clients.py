"""
===========================================================
Create the clients page of the app
===========================================================
Script purpose:
    This script's purpose is to create the clients page of the app;
    this is where advisors can input the clients name and credentials, details, etc.
    
"""

import streamlit as st
import pandas as pd
from utils.db_connection import connect_to_database
from utils.queries import get_clients, add_client, delete_client

if not st.session_state.get("logged_in"):
    st.switch_page("main.py")

st.title("Clients")

clients = get_clients()

if len(clients) == 0:
    st.info("No clients yet. Add one below!")
else:
    for client in clients:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(client[1])
        with col2:
            if st.button("View", key=client[0]):
                st.session_state["selected_client_id"] = client[0]
                st.session_state["selected_client_name"] = client[1]
                st.switch_page("pages/02_client_detail.py")
        with col3:
            if st.button("Delete", key=f"delete_{client[0]}"):
                st.session_state["confirm_delete"] = client[0]

if st.session_state.get("confirm_delete"):
    client_id_to_delete = st.session_state["confirm_delete"]
    st.warning(f"Are you sure you want to delete this client? This will delete all their data")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, delete"):
            delete_client(client_id_to_delete)
            st.session_state["confirm_delete"] = None
            st.success("Client deleted!")
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state["confirm_delete"] = None
            st.rerun()

st.subheader("Add New Client")
with st.form("add_client_form"):
    full_name = st.text_input("Client Full Name")
    submitted = st.form_submit_button("Add Client")
    if submitted:
        if full_name.strip() == "":
            st.error("Please enter a name...")
        else:
            add_client(full_name)
            st.success(f"{full_name} added successfully!!")
            st.rerun()