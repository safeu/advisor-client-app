# Advisor Client App

A web application built for insurance advisors to manage and track client policies, payments, and fund allocations.

## Features
- Add and manage clients
- Track policy details, billing, and fund allocation
- Record and edit transaction history by year
- View missed and due payments at a glance on the home dashboard

## Tech Stack
- **Python** — core language
- **Streamlit** — web app framework
- **PostgreSQL (Supabase)** — cloud database
- **Pandas** — data manipulation
- **psycopg2** — PostgreSQL connector

## Folder Structure
```
Advisor_Client_App/
├── main.py
├── requirements.txt
├── .gitignore
├── config/
│   └── .env
├── database/
│   └── schema.sql
├── pages/
│   ├── 01_clients.py
│   └── 02_client_detail.py
└── utils/
    ├── db_connection.py
    └── queries.py
```

## Getting Started

### 1. Clone the repository
```
git clone https://github.com/safeu/advisor-client-app.git
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `config/.env` file with your Supabase credentials:
```
DB_HOST=your_host
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

### 4. Set up the database
Run `database/schema.sql` in your Supabase SQL Editor to create the tables.

### 5. Run the app
```
python -m streamlit run main.py
```

## Deployment
This app is deployed on Streamlit Community Cloud. Add your Supabase credentials in the Streamlit Cloud secrets settings before deploying.