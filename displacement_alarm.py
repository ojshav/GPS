import math
import sqlite3
import pandas as pd
from opencage.geocoder import OpenCageGeocode
import time

def get_address(latitude, longitude):
    key = '48ea843836994f04b8174c84402dea69'  # Replace with your OpenCage API key
    geocoder = OpenCageGeocode(key)
    result = geocoder.reverse_geocode(latitude, longitude)
    return result[0]['formatted'] if result else "Address not found"

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    :param lat1, lon1: Latitude and longitude of the first point
    :param lat2, lon2: Latitude and longitude of the second point
    :return: Distance in kilometers
    """
    R = 6371  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def displacement_alarm(threshold_km=1, db_name="gps_data.db"):
    """
    Check for significant displacement between successive GPS data points.
    :param threshold_km: Threshold displacement in kilometers
    :param db_name: Name of the SQLite database file
    :return: List of vehicles with significant displacement
    """
    connection = sqlite3.connect(db_name)
    query = "SELECT * FROM gps_data ORDER BY timestamp"
    data = pd.read_sql_query(query, connection)
    connection.close()

    alerts = []
    for i in range(1, len(data)):
        prev = data.iloc[i - 1]
        current = data.iloc[i]
        distance = haversine(prev['latitude'], prev['longitude'], current['latitude'], current['longitude'])
        
        if distance > threshold_km:
            previous_address = get_address(prev['latitude'], prev['longitude'])  # Get address for previous location
            current_address = get_address(current['latitude'], current['longitude'])  # Get address for current location
            
            alerts.append({
                "tracker_id": current["tracker_id"],
                "prev_location": (prev['latitude'], prev['longitude']),
                "current_location": (current['latitude'], current['longitude']),
                "displacement_km": round(distance, 2),
                "previous_address": previous_address,  # Add previous address
                "current_address": current_address,    # Add current address
            })

    if not alerts:
        print(f"No displacements above {threshold_km} km detected.")
    else:
        print(f"Displacements above {threshold_km} km detected:")
        for alert in alerts:
            print(alert)
    return alerts  # Return the alerts list with addresses and distances

# Example usage
displacements = displacement_alarm(threshold_km=1)
