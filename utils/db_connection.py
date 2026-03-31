"""
===========================================================
Setting up database connection
===========================================================
Script purpose:
    Script to connect to the database.  
"""


import psycopg2
import streamlit as st
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path="config/.env")

def connect_to_database():
    try:
        try:
            conn = psycopg2.connect(
                host=st.secrets["DB_HOST"],
                database=st.secrets["DB_NAME"],
                user=st.secrets["DB_USER"],
                password=st.secrets["DB_PASSWORD"],
                port=st.secrets["DB_PORT"]
            )
        except Exception:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to the Database: {e}")
        raise