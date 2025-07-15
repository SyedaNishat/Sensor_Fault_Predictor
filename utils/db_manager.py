import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.getcwd(), "sensor_faults.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)  # Use the same path
    cursor = conn.cursor()

    # 🔥 Drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS sensor_data")

    # ✅ Recreate with updated columns
    cursor.execute("""
        CREATE TABLE sensor_data (
            Timestamp TEXT,
            Sensor TEXT,
            Value REAL,
            FaultType TEXT,
            Severity TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_sensor_data(df: pd.DataFrame):
    """Insert processed DataFrame into the SQLite DB."""
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('sensor_data', conn, if_exists='append', index=False)
    conn.close()

def fetch_sensor_data():
    """Fetch all sensor data from DB."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sensor_data", conn)
    conn.close()
    return df

def clear_sensor_data():
    """Clear all data (for testing/demo/reset)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sensor_data")
    conn.commit()
    conn.close()
