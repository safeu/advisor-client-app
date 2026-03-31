"""
===========================================================
Scripts for querying data
===========================================================
Script purpose:
    Query the data needed for 02_client_detail.py file. 

"""

from utils.db_connection import connect_to_database
import logging

logger = logging.getLogger(__name__)

def get_policy(client_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM policies WHERE client_id = %s", (client_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        logger.error(f"Error fetching policy data: {e}")
        raise

def get_fund_info(policy_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fund_info WHERE policy_id = %s ORDER BY as_of_date DESC LIMIT 1", (policy_id,))
        rows = cursor.fetchone()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error fetching fund info: {e}")
        raise

def get_riders(policy_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM riders WHERE policy_id = %s", (policy_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error fetching riders data: {e}")
        raise

def get_payments(policy_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE policy_id = %s ORDER BY year_number ASC, due_date ASC", (policy_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error fetching payments data: {e}")
        raise

def update_policy(policy_id, data):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
                UPDATE policies SET
                    plan_name = %s,
                    policy_number = %s,
                    issue_date = %s,
                    face_amount = %s,
                    sum_assured = %s,
                    policy_duration = %s,
                    years_to_pay = %s,
                    remaining_years = %s,
                    status = %s,
                    premium_due = %s,
                    mode_of_payment = %s,
                    premium_amount = %s,
                    total_annual_premium = %s
                WHERE id = %s
        """, (*data, policy_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error updating policy data: {e}")
        raise

def update_payment(payment_id, due_date, amount, date_paid, status):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
                UPDATE payments SET
                    due_date = %s,
                    amount = %s,
                    date_paid = %s,
                    status = %s
                WHERE id = %s
        """, (due_date, amount, date_paid, status, payment_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error updating payment data: {e}")
        raise

def add_payment(policy_id, year_number, due_date, amount, date_paid, status):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO payments (policy_id, year_number, due_date, amount, date_paid, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (policy_id, year_number, due_date, amount, date_paid, status))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error adding payment data: {e}")
        raise


def update_fund_info(fund_id, current_fund_value, fund_name, fund_allocation_pct, cost_of_insurance, as_of_date):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fund_info SET
                current_fund_value = %s, 
                fund_name = %s,
                fund_allocation_pct = %s,
                cost_of_insurance = %s, 
                as_of_date = %s
            WHERE id = %s
        """, (current_fund_value, fund_name, fund_allocation_pct, cost_of_insurance, as_of_date, fund_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error updating fund info: {e}")
        raise

def add_policy(client_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO policies (client_id) VALUES (%s)", (client_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error adding policy: {e}")
        raise

def add_fund_info(policy_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO fund_info (policy_id) VALUES (%s)", (policy_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error adding fund info: {e}")
        raise

def add_rider(policy_id, rider_name, amount):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO riders (policy_id, rider_name, amount) VALUES (%s, %s, %s)",
            (policy_id, rider_name, amount))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error adding rider: {e}")
        raise



### HOME PAGE QUeries
def total_clients():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        logger.error(f"Error getting total clients: {e}")
        raise

def total_missed_payments():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'Missed'")
        rows = cursor.fetchone()
        cursor.close()
        conn.close()
        return rows
    
    except Exception as e:
        logger.error(f"Error getting total missed payments: {e}")
        raise


def total_payments_due():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'DUE'")
        rows = cursor.fetchone()
        cursor.close()
        conn.close()
        return rows
    
    except Exception as e:
        logger.error(f"Error getting total due payments: {e}")
        raise