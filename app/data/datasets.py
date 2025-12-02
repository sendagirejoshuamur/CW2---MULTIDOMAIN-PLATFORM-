import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path
from app.data.db import connect_database


def insert_into_datasets(dataset_id,name,rows,columns,uploaded_by,upload_date):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO datasets_metadata
    (dataset_id,name,rows,columns,uploaded_by,upload_date)
    VALUES(?, ?, ?, ?, ?, ?)
    """, (dataset_id,name,rows,columns,uploaded_by,upload_date))

    conn.commit()
    cursor.close()

def delete_from_datasets(dataset_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM datasets_metadata WHERE dataset_id = ?
    """, (dataset_id,)
                   )
    conn.commit()
    cursor.close()

def get_all_datasets():
    """Get all datasets"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata ORDER BY upload_date DESC")
    results = cursor.fetchall()
    cursor.close()
    return results

def get_dataset_by_id(dataset_id):
    """Get specific dataset by ID"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata WHERE dataset_id = ?", (dataset_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

def get_large_datasets():
    """Get datasets with more than 10,000 rows"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata WHERE rows > 10000 ORDER BY rows DESC")
    results = cursor.fetchall()
    cursor.close()
    return results

def get_old_datasets():
    """Get datasets older than 6 months"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM datasets_metadata 
        WHERE JULIANDAY('now') - JULIANDAY(upload_date) > 180
        ORDER BY upload_date ASC
    """)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_user_datasets(username):
    """Get all datasets uploaded by a user"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata WHERE uploaded_by = ?", (username,))
    results = cursor.fetchall()
    cursor.close()
    return results

def get_dataset_stats():
    """Get basic dataset statistics"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_datasets,
            SUM(rows) as total_rows,
            AVG(rows) as avg_rows
        FROM datasets_metadata
    """)
    result = cursor.fetchone()
    cursor.close()
    return result

def get_recent_uploads(limit=10):
    """Get most recent dataset uploads"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata ORDER BY upload_date DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    cursor.close()
    return results

