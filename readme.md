Bitespeed Identity Reconciliation API

A backend service built using FastAPI and PostgreSQL to identify and reconcile customer contacts based on email and phone number.

This service consolidates duplicate contact information into a single primary contact with linked secondary contacts.

Project Structure

bitespeed/
│
├── main.py           # FastAPI application
├── database.py       # Database connection & session management
├── models.py         # SQLAlchemy models
├── .env              # Environment variables
├── requirements.txt
└── README.md

Setup Instructions

1️⃣ Clone the repository
git clone <your-repo-url>
cd bitespeed

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies & requirements.txt
pip install -r requirements.txt
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv

4️⃣ Configure Environment Variables
Create a .env file in root folder:

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bitespeed

5️⃣ Create PostgreSQL Database
Using pgAdmin or psql:

CREATE DATABASE bitespeed;


▶️ Run the Application
uvicorn main:app --reload