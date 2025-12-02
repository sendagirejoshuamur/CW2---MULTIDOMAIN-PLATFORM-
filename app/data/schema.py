import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path


def create_users_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE COLLATE BINARY NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    conn.commit()


def create_cyber_incidents_table(conn):
    """Creating cyber incidents table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id TEXT PRIMARY KEY,
            timestamp TIMESTAMP TEXT,
            severity TEXT,
            category TEXT, 
            status TEXT,
            description TEXT,
            reported_by TEXT
        )
    """)
    conn.commit()

def create_datasets_metadata_table(conn):
    """Creating the datasets_metadata table"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            rows INTEGER NOT NULL,
            columns INTEGER NOT NULL,
            uploaded_by TEXT NOT NULL,
            upload_date DATE NOT NULL,
            FOREIGN KEY (uploaded_by) REFERENCES users(username)
        )
    """)
    conn.commit()

def create_it_tickets_table(conn):
    """Create IT tickets table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id INTEGER PRIMARY KEY,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolution_time_hours INTEGER
        )
    """)
    conn.commit()

def create_uploads_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

# Creating all tables
def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    create_uploads_table(conn)



DB_PATH = Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA") / "intelligence_platform.db"

conn = sqlite3.connect(DB_PATH)
create_all_tables(conn)