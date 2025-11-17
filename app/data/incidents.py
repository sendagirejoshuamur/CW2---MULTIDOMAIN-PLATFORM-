import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path
from app.data.db import connect_database


def insert_incident(incident_id, timestamp, severity, category, status, description, reported_by):
    # inserting into the incidents table
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cyber_incidents 
    (incident_id, timestamp, severity, category, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (incident_id, timestamp, severity, category, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


def get_all_incidents():
    # function to get all incidents as a data frame
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY incident_id DESC ", conn)
    conn.close()
    return df

def get_incident_by_id(incident_id):
    # function to get incidents by id
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        (incident_id,),
    )

    incident = cursor.fetchone()
    conn.close()
    return incident


def get_incident_by_type(incident_type):
    # function to get incidents by type
    conn = connect_database()
    cursor = conn.cursor()

    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE incident_type = ? ORDER BY DESC",
        conn,
        params=(incident_type,)
    )
    conn.close()
    return df

def get_incident_by_severity(severity):
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE severity = ? ORDER BY DESC",
        conn,
        params=(severity,)
    )
    conn.close()
    return df


def update_incident_status(incident_id, new_status):
    # function to update incident status
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    return row_count

def delete_incident(incident_id):
    # function to delete incident
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    return row_count

def get_incidents_by_status(status):
    # function to get incidents by status
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE status = ? ORDER BY timestamp DESC",
        conn,
        params=(status,)
    )
    conn.close()
    return df

def get_incident_stats():
    # function to get incident statistics
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT 
            severity,
            status,
            COUNT(*) as count
        FROM cyber_incidents 
        GROUP BY severity, status
        ORDER BY severity, status
    """, conn)
    conn.close()
    return df

def search_incidents(search_term):
    # function to search incidents by description
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE description LIKE ? ORDER BY timestamp DESC",
        conn,
        params=(f'%{search_term}%',)
    )
    conn.close()
    return df
