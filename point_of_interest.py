from haversine import haversine
from realtime_Data import fetch_all_data
import folium

def point_of_interest_mapping(pois, radius_km=0.5, db_name="gps_data.db"):
    """
    Check if vehicles are near defined points of interest (POIs).
    :param pois: List of tuples (latitude, longitude) representing POIs
    :param radius_km: Radius around POI in kilometers
    :param db_name: Name of the SQLite database file
    :return: List of vehicles near POIs
    """
    data = fetch_all_data(db_name)
    nearby_vehicles = []
    for poi in pois:
        for _, row in data.iterrows():
            vehicle_location = (row['latitude'], row['longitude'])
            distance = haversine(poi, vehicle_location)
            if distance <= radius_km:
                nearby_vehicles.append({
                    "tracker_id": row["tracker_id"],
                    "location": (row['latitude'], row['longitude']),
                    "poi": poi,
                    "distance_km": round(distance, 2)
                })

    if not nearby_vehicles:
        print(f"No vehicles within {radius_km} km of POIs.")
    else:
        print(f"Vehicles within {radius_km} km of POIs:")
        for vehicle in nearby_vehicles:
            print(vehicle)
    return nearby_vehicles

def visualize_pois(pois, map_name="pois_map.html"):
    """
    Visualize points of interest (POIs) on a map.
    :param pois: List of tuples (latitude, longitude, name) representing POIs
    :param map_name: Name of the HTML file to save the map
    """
    # Check if there are any POIs to display
    if not pois:
        print("No points of interest to display.")
        return

    # Create a map centered around the average location of the POIs
    avg_lat = sum(poi[0] for poi in pois) / len(pois)
    avg_lon = sum(poi[1] for poi in pois) / len(pois)
    map_ = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Add POIs to the map
    for poi in pois:
        folium.Marker(
            location=[poi[0], poi[1]],
            popup=poi[2],  # Name of the POI
            icon=folium.Icon(color='blue')
        ).add_to(map_)

    # Attempt to save the map to an HTML file
    try:
        map_.save(map_name)
        print(f"Map has been saved as '{map_name}'.")
    except Exception as e:
        print(f"An error occurred while saving the map: {e}")

# Example POIs and usage
pois = [(28.6139, 77.2090), (28.7041, 77.1025)]  # Example: Delhi locations
near_pois = point_of_interest_mapping(pois, radius_km=500)
