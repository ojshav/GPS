import sqlite3
import pandas as pd

def fetch_all_data(db_name="gps_data.db"):
    """
    Fetch all GPS data from the database.
    :param db_name: Name of the SQLite database file
    :return: DataFrame containing all GPS data
    """
    connection = sqlite3.connect(db_name)
    query = "SELECT * FROM gps_data"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

def fetch_data_by_condition(condition, db_name="gps_data.db"):
    """
    Fetch GPS data from the database based on a condition.
    :param condition: SQL condition as a string (e.g., "speed > 100")
    :param db_name: Name of the SQLite database file
    :return: DataFrame containing filtered GPS data
    """
    connection = sqlite3.connect(db_name)
    query = f"SELECT * FROM gps_data WHERE {condition}"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

def fetch_data_by_tracker_id(tracker_id, db_name="gps_data.db"):
    """
    Fetch GPS data from the database for a specific vehicle.
    :param tracker_id: Tracker ID of the vehicle
    :param db_name: Name of the SQLite database file
    :return: DataFrame containing GPS data for the specified vehicle
    """
    connection = sqlite3.connect(db_name)
    query = f"SELECT * FROM gps_data WHERE tracker_id = '{tracker_id}'"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

# Fetch and display all data
print("Fetching all data...")
all_data = fetch_all_data()
print(all_data)


