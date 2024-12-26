from data import gps_data
import sqlite3

def setup_database(db_name="gps_data.db"):
    """
    Set up an SQLite database and create a table for GPS data.
    :param db_name: Name of the SQLite database file
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gps_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracker_id TEXT,
            latitude REAL,
            longitude REAL,
            speed REAL,
            timestamp TEXT,
            status TEXT,
            power_status TEXT
        )
    """)
    connection.commit()
    connection.close()

def insert_data_into_db(gps_data, db_name="gps_data.db"):
    """
    Insert GPS data into the SQLite database.
    :param gps_data: List of dictionaries containing GPS data
    :param db_name: Name of the SQLite database file
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    for record in gps_data:
        # Convert Decimal values to float
        record['latitude'] = float(record['latitude'])
        record['longitude'] = float(record['longitude'])
        record['speed'] = float(record['speed'])
        cursor.execute("""
            INSERT INTO gps_data (tracker_id, latitude, longitude, speed, timestamp, status, power_status)
            VALUES (:tracker_id, :latitude, :longitude, :speed, :timestamp, :status, :power_status)
        """, record)
    connection.commit()
    connection.close()

# Setup database and insert data
setup_database()
insert_data_into_db(gps_data)
print("Data inserted into the database successfully.")
