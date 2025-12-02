import pathlib

from app.data.db import connect_database
from app.data.schema import create_all_tables, conn
from app.services.user_service import*
from app.data.incidents import insert_incident, get_all_incidents
from app.data.csv_loaders import load_all_csv_data
from app.data.tickets import*
from app.data.datasets import *
from pathlib import Path
from app.data.users import*

def csv():

    # Loading  CSV data
    print("Loading CSV data...")
    conn = connect_database()
    total_rows = load_all_csv_data(conn)
    conn.close()
    print(f"       Loaded {total_rows} total rows from CSV files")

# def main():
#     print("=" * 60)
#     print("Week 8: Database Demo")
#     print("=" * 60)
#
#     # 1. Setup database
#     conn = connect_database()
#     create_all_tables(conn)
#     conn.close()
#
#     # filepath = pathlib.Path("DATA") / "users.txt"
#
#      # 2. Migrate users
#     migrate_users_from_file(filepath)
#
#
#     #
#     # 3. Test authentication
#     # success, msg = register_user("alice", "SecurePass123!", "analyst")
#     # print(msg)
#     # #
#     # success, msg = login_user("alice", "SecurePass123!")
#     # print(msg)
#
#     # incident_id = insert_incident(
#     #     "2024-11-05",  # This should be incident_id, but looks like a timestamp
#     #     "Phishing",  # This should be timestamp, but looks like category
#     #     "High",  # This should be severity, but looks correct
#     #     "Open",  # This should be category, but looks like status
#     #     "Suspicious email detected",  # This should be status, but looks like description
#     #     "alice",  # This should be description, but looks like reported_by
#     #     "your_incident_id_here",  # This should be reported_by, but looks like incident_id
#     # )
#
#     # 4. Test CRUD
#     # incident_id = insert_incident(
#     #     "1000",  # incident_id
#     #     "2024-01-15 09:30:00",  # timestamp
#     #     "High",  # severity
#     #     "Phishing",  # category
#     #     "Open",  # status
#     #     "Suspicious email detected",  # description
#     #     "alice"  # reported_by
#     # )
#     # print(f"Created incident #{incident_id}")
#
#     # ticket_id = insert_into_tickets(
#     #     "9111",  # ticket_id
#     #     "High",  # priority
#     #     "sj needs a first class",  # description
#     #     "Open",  # status
#     #     "John sj",  # assigned_to
#     #     "2024-01-15 10:00:00",  # created_at
#     #     "72"  # resolution_time_hours
#     # )
#     # print(f"inserted into Ticket ID: {ticket_id}")
#
#     # deleted the ticket
#     # delete_tickets(9111)
#
#     # Query data
#     # df = get_all_incidents()
#     # print(f"Total incidents: {len(df)}")
#
#
#     # insert_into_datasets(
#     #     "91",
#     #     "sj",
#     #     "9000",
#     #     "1009",
#     #     "it_sj",
#     #     "00/00/2000"
#     # )
#
#     delete_from_datasets(91)
#
# def mainn():
#
#     print("=" * 60)
#     print("User Migration Test")
#     print("=" * 60)
#
#     # 1️⃣ Reset users table (temporary)
#     conn = connect_database()
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS users")
#     conn.commit()
#     conn.close()
#     print("Users table has been reset.")
#
#     # 2️⃣ Recreate all tables
#     conn = connect_database()
#     create_all_tables(conn)
#     conn.close()
#
#     # 3️⃣ Migrate users
#     migrate_users_from_file("DATA/users.txt")
#
#     insert_user()
#
#
# def sj():
#     users = [
#         ("Admin", "Admin123!", "admin"),
#         ("analyst1", "Analyst123!", "analyst"),
#         ("analyst2", "Analyst234!", "analyst"),
#         ("user5", "User123!", "user"),
#         ("user17", "User234!", "user"),
#         ("user10", "User345!", "user"),
#     ]
#
#     for username, password, role in users:
#         password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#         if insert_user(username, password_hash, role):
#             print(f"Inserted user: {username}")
#         else:
#             print(f"Failed to insert user: {username}")
#
# def run():
#     # password_hash = "sss"
#     # insert_user("Admin", password_hash, "admin")
#     filepath = Path("DATA/users.txt")
#     migrate_users_from_file(filepath)
#
#
# # def lop():
# #     filepath = Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA\users.txt")
# #     print("Checking file:", filepath)
# #     print("Exists:", filepath.exists())
# #
# #     if not filepath.exists():
# #         print("File not found!")
# #     else:
# #         with open(filepath, "r", encoding="utf-8") as f:
# #             for line in f:
# #                 print("Raw line:", repr(line))
# #
# #     filepath = Path("DATA/users.txt")
# #     if not filepath.exists():
# #         print(f"File not found: {filepath}")
# #     else:
# #         with open(filepath, "r") as f:
# #             for line in f:
# #                 line = line.strip()
# #                 if not line or line.startswith("#"):
# #                     continue  # Skip empty lines or comments
# #
# #                 parts = line.split(",")
# #                 if len(parts) < 2:
# #                     print(f"Invalid line (skipped): {line}")
# #                     continue
# #
# #                 username = parts[0].strip()
# #                 password_hash = parts[1].strip()
# #                 role = parts[2].strip() if len(parts) > 2 else "user"
# #
# #                 print(f"Username: {username}, Password Hash: {password_hash}, Role: {role}")
#
#
#
# def connect_database():
#     import sqlite3, os
#     db_path = "DATA/intelligence_platform.db"  # or your path
#     print("Connecting to DB at:", os.path.abspath(db_path))
#     return sqlite3.connect(db_path)
#
if __name__ == "__main__":
    # lop()
    # sj()
    # run()
    # connect_database()
    # main()
    csv()
    #  mainn()



#
