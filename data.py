import random
from faker import Faker
import datetime
import pandas as pd

def generate_gps_data(num_records=20, tracker_id="TRACKER_1000"):
    """
    Generate dummy GPS data for a single vehicle with fields like latitude, longitude, speed, timestamp, and status.
    :param num_records: Number of records to generate
    :param tracker_id: Fixed tracker ID for the vehicle
    :return: List of dictionaries representing GPS data
    """
    fake = Faker()
    gps_data = []
    
    # Define the latitude and longitude ranges for Delhi, Noida, and Gurgaon
    lat_range = (28.4, 28.8)  # Approximate latitude range
    lon_range = (76.8, 77.3)  # Approximate longitude range
    
    for i in range(num_records):
        record = {
            "tracker_id": tracker_id,  # Fixed tracker ID for one vehicle
            "latitude": round(random.uniform(lat_range[0], lat_range[1]), 6),  # Random latitude
            "longitude": round(random.uniform(lon_range[0], lon_range[1]), 6),  # Random longitude
            "speed": round(random.uniform(0, 120), 2),  # Speed in km/h
            "timestamp": (datetime.datetime.now() + datetime.timedelta(minutes=i)).isoformat(),  # Increment timestamp
            "status": random.choice(["Moving", "Idle", "Stopped"]),  # Random status
            "power_status": random.choice(["On", "Off"]),  # Simulating power status
        }
        gps_data.append(record)
    
    return gps_data

# Generate and preview data
gps_data = generate_gps_data(20)  # Generate 20 records
print(pd.DataFrame(gps_data))
