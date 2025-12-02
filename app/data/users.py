import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path
from app.data.db import connect_database

# function to get all the usernames from the database
def get_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE username = ?", (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()


def get_all_users():
    # fuction to get all users
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

    conn.commit()
    conn.close()

def clear_users_table():
    conn = connect_database()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")  # reset ID counter
        conn.commit()
        print("Users table cleared and ID counter reset.")
    except Exception as e:
        print("Error clearing users table:", e)
    finally:
        conn.close()


def clear_database():
    """
    Deletes all data from all main tables in the database
    and resets their auto-increment IDs.
    """
    conn = connect_database()
    cursor = conn.cursor()

    try:
        # List all main tables
        tables = ["users", "cyber_incidents", "it_tickets", "datasets_metadata"]

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")  # reset autoincrement

        conn.commit()
        return True

    except Exception as e:
        print("Error clearing database:", e)
        return False

    finally:
        conn.close()
