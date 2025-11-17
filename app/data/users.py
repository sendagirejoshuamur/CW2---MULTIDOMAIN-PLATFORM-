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
    # function to insert a new user
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()


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

