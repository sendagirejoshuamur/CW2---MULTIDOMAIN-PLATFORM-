import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path
from app.data.db import connect_database


def insert_into_tickets(ticket_id,priority,description,status,assigned_to,created_at,resolution_time_hours):
    # function to insert into tickets
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO it_tickets
    (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
    VALUES(?, ?, ?, ?, ?, ?, ?)
    """,(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
    )

    conn.commit()
    cursor.close()

def delete_tickets(ticket_id):
    # function to delte tickets by ticket id
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM it_tickets WHERE ticket_id = ?
    """,(ticket_id,)
    )

    conn.commit()
    cursor.close()
    row_count = cursor.rowcount

    return row_count


