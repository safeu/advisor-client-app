/*
===========================================================
Create database schema for the application.
===========================================================
Script purpose:
    This script creates database schemas for the database created in PostgreSQL
    (Supabase)

Warning:
    If this script is ran... it would delete/drop all the tables and create a new one.
    Leading to deletion of all data within the table.
    
    Delete the DROP TABLE commands if needed.
*/

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS riders;
DROP TABLE IF EXISTS fund_info;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS clients;

--for client details
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


-- the policty details
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(id) ON DELETE CASCADE,
    plan_name VARCHAR(200),
    policy_number VARCHAR(100) UNIQUE,
    issue_date DATE,
    face_amount NUMERIC(15,2),
    sum_assured NUMERIC(15,2),
    policy_duration VARCHAR(100),
    years_to_pay VARCHAR(50),
    remaining_years VARCHAR(50),
    status VARCHAR(50),
    premium_due DATE,
    mode_of_payment VARCHAR(50),
    premium_amount NUMERIC(15,2),
    total_annual_premium NUMERIC(15,2),
    created_at TIMESTAMP DEFAULT NOW()
);


-- for fund infos
CREATE TABLE fund_info (
    id SERIAL PRIMARY KEY,
    policy_id INT REFERENCES policies(id) ON DELETE CASCADE,
    current_fund_value NUMERIC(15,2),
    fund_name VARCHAR(200),
    fund_allocation_pct NUMERIC(5,2),
    cost_of_insurance NUMERIC(15,2),
    as_of_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);



-- for policy rider
CREATE TABLE riders (
    id SERIAL PRIMARY KEY,
    policy_id INT REFERENCES policies(id) ON DELETE CASCADE,
    rider_name VARCHAR(200),
    amount NUMERIC(15,2),
    is_active BOOLEAN DEFAULT TRUE
);


-- for transaction history
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    policy_id INT REFERENCES policies(id) ON DELETE CASCADE,
    year_number INT,
    due_date DATE,
    amount NUMERIC(15,2),
    date_paid DATE,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);