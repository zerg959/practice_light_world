#!/usr/bin/env python
"""
Drop tables and users.
"""
import os
import sys
import psycopg
from pathlib import Path
from dotenv import load_dotenv

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
SUPERUSER_PASSWORD = os.getenv('POSTGRES_SUPERUSER_PASSWORD', 'postgres')


def reset_database():
    print(f"Reset DB: {DB_NAME}")
    print(f"Reset user: {DB_USER}")
    
    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Denied")
        return

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
        print(f"Connection err: {e}")
        sys.exit(1)

    # 1. Close all connections with DB
    cur.execute(f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{DB_NAME}'
        AND pid <> pg_backend_pid()
    """)

    # 2. Drop DB
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    print(f"DB {DB_NAME} dropped")

    # 3. Check if user exists
    cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname = '{DB_USER}'")
    if cur.fetchone():
        # 4. Ecall all dependencies before drop user
        try:
            # Transfer all to SU
            cur.execute(f"REASSIGN OWNED BY {DB_USER} TO postgres")
            # Delete user permissions
            cur.execute(f"DROP OWNED BY {DB_USER}")
            # Drop role
            cur.execute(f"DROP ROLE IF EXISTS {DB_USER}")
            print(f"User {DB_USER} dropped")
        except Exception as e:
            print(f"Cant find user: {e}")
            print("💡 Try: sudo -u postgres psql -c 'DROP ROLE {DB_USER};'")
    else:
        print(f"User {DB_USER} doesnt exist")

    cur.close()
    conn.close()
    print("\n Dropped! Run: python create_db.py")


if __name__ == '__main__':
    reset_database()