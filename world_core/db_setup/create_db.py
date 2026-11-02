#!/usr/bin/env python
"""
Create PostgreSQL.
Use Psycopg 3 (psycopg[binary]).
"""
import os
import sys
import psycopg 
from pathlib import Path
from dotenv import load_dotenv

# Find .env in project root 
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

if not env_path.exists():
    print(f"File .env not found: {env_path}")
    sys.exit(1)

load_dotenv(env_path)

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Superuser-postgres password
SUPERUSER_PASSWORD = os.getenv('POSTGRES_SUPERUSER_PASSWORD', 'postgres')


def create_database():
    print(f"Create DB: {DB_NAME}")
    print(f"User: {DB_USER}")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    print()

    # Connect to service DB-postgres
    try:
        conn = psycopg.connect(
            dbname='postgres',
            user='postgres',
            password=SUPERUSER_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            autocommit=True  
        )
        cur = conn.cursor()
    except Exception as e:
        print(f"Connection error PostgreSQL: {e}")
        print("Check if PostgreSQL is running: sudo service postgresql start")
        sys.exit(1)

    # Create user
    cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname = '{DB_USER}'")
    if not cur.fetchone():
        cur.execute(f"CREATE ROLE {DB_USER} WITH LOGIN PASSWORD '{DB_PASSWORD}'")
        print(f"User {DB_USER} created")
    else:
        print(f"User {DB_USER} already exists")

    # Create DB
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER} ENCODING 'UTF8'")
        print(f"DB {DB_NAME} created")
    else:
        print(f"DB {DB_NAME} already exists")

    # Set parameters
    cur.execute(f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8'")
    cur.execute(f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed'")
    cur.execute(f"ALTER ROLE {DB_USER} SET timezone TO 'UTC'")

    # Set permissions
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
    cur.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER}")

    cur.close()
    conn.close()

    print()
    print("Run DB:")
    print("python manage.py migrate")


if __name__ == '__main__':
    create_database()