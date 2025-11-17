from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.csv_loaders import load_all_csv_data


def csv():

    # Loading  CSV data
    print("Loading CSV data...")
    conn = connect_database()
    total_rows = load_all_csv_data(conn)
    conn.close()
    print(f"       Loaded {total_rows} total rows from CSV files")

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    migrate_users_from_file()
    #
    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    #
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # incident_id = insert_incident(
    #     "2024-11-05",  # This should be incident_id, but looks like a timestamp
    #     "Phishing",  # This should be timestamp, but looks like category
    #     "High",  # This should be severity, but looks correct
    #     "Open",  # This should be category, but looks like status
    #     "Suspicious email detected",  # This should be status, but looks like description
    #     "alice",  # This should be description, but looks like reported_by
    #     "your_incident_id_here",  # This should be reported_by, but looks like incident_id
    # )

    # 4. Test CRUD
    # incident_id = insert_incident(
    #     "1000",  # incident_id
    #     "2024-01-15 09:30:00",  # timestamp
    #     "High",  # severity
    #     "Phishing",  # category
    #     "Open",  # status
    #     "Suspicious email detected",  # description
    #     "alice"  # reported_by
    # )
    # print(f"Created incident #{incident_id}")

    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")


if __name__ == "__main__":
    main()
    csv()