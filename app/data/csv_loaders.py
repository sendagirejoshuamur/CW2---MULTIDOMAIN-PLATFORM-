import pandas as pd
from pathlib import Path
from app.data.db import connect_database


def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    """
    # path().exists checks if the file path exsits
    if not Path(csv_path).exists():
        print(f"the CSV file is not found: {csv_path}")
        return 0

    try:
        # converting our csv file to pandas
        df = pd.read_csv(csv_path)
        row_count = len(df)

        # Clear existing data
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        print(f" XX Cleared existing data from {table_name}")

        # Load fresh data
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )

        print(f"(-_-) Loaded {row_count} rows into {table_name} table from {csv_path.name}")
        return row_count

    except Exception as e:
        print(f"XX Error loading {csv_path}: {e}")
        return 0



def load_all_csv_data(conn):
    """
    Load all CSV files into their respective tables.

    Args:
        conn: Database connection

    Returns:
        int: Total number of rows loaded
    """
    # DB_PATH = Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA")
    data_dir = Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA")
    total_rows = 0

    # Map CSV files to their tables using a dictionary
    csv_mappings = {
        'cyber_incidents.csv': 'cyber_incidents',
        'datasets_metadata.csv': 'datasets_metadata',
        'it_tickets.csv': 'it_tickets'
    }

    for csv_file, table_name in csv_mappings.items():
        csv_path = data_dir / csv_file
        if csv_path.exists():
            rows_loaded = load_csv_to_table(conn, csv_path, table_name)
            total_rows += rows_loaded
        else:
            print(f"CSV file not found: {csv_file}")

    return total_rows