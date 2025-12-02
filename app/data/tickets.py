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

def get_all_tickets():
    """Get all tickets"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets ORDER BY created_at DESC")
    results = cursor.fetchall()
    cursor.close()
    return results

def get_ticket_by_id(ticket_id):
    """Get specific ticket by ID"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

def get_tickets_by_status(status):
    """Get all tickets with specific status"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets WHERE status = ?", (status,))
    results = cursor.fetchall()
    cursor.close()
    return results

def get_tickets_by_assignee(assigned_to):
    """Get all tickets assigned to specific staff"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets WHERE assigned_to = ?", (assigned_to,))
    results = cursor.fetchall()
    cursor.close()
    return results

def update_ticket_status(ticket_id, status):
    """Update ticket status"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id))
    conn.commit()
    cursor.close()

def assign_ticket(ticket_id, assigned_to):
    """Assign ticket to staff member"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET assigned_to = ? WHERE ticket_id = ?", (assigned_to, ticket_id))
    conn.commit()
    cursor.close()

# Analysis functions to find bottlenecks:
def get_slowest_status():
    """Find which status has the most tickets stuck"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) as ticket_count 
        FROM it_tickets 
        WHERE status != 'Resolved' 
        GROUP BY status 
        ORDER BY ticket_count DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_slowest_staff():
    """Find which staff has the most unresolved tickets"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT assigned_to, COUNT(*) as ticket_count 
        FROM it_tickets 
        WHERE status != 'Resolved' AND assigned_to IS NOT NULL
        GROUP BY assigned_to 
        ORDER BY ticket_count DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_avg_resolution_time():
    """Get average resolution time by priority"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT priority, AVG(resolution_time_hours) as avg_hours 
        FROM it_tickets 
        WHERE resolution_time_hours IS NOT NULL
        GROUP BY priority 
        ORDER BY avg_hours DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_oldest_pending_tickets(limit=10):
    """Get oldest unresolved tickets"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM it_tickets 
        WHERE status != 'Resolved' 
        ORDER BY created_at ASC 
        LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
    cursor.close()
    return results


