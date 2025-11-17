import sqlite3
from pathlib import Path

DB_PATH = Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""

    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))


connect_database(DB_PATH)





