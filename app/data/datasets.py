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

