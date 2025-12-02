
from app.services.user_service import connect_database


def clear_uploads_table():
    """
    Clears all records from the uploads table.
    """
    try:
        conn = connect_database()
        cursor = conn.cursor()

        # Delete all rows
        cursor.execute("DELETE FROM uploads")

        # Commit changes
        conn.commit()
        conn.close()

        print("Uploads table cleared successfully.")
        return True
    except Exception as e:
        print(f"Error clearing uploads table: {e}")
        return False
