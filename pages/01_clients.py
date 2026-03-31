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

st.title("Clients")


def get_clients():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, created_at FROM clients ORDER BY full_name ASC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_client(full_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (full_name) VALUES (%s)", (full_name,))
    conn.commit()
    cursor.close()
    conn.close()

clients = get_clients()

if len(clients) == 0:
    st.info("No clients yet. Add one below!")
else:
    df = pd.DataFrame(clients, columns=["ID", "Name", "Date Added"])
    st.dataframe(df, use_container_width=True)


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