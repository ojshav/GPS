from realtime_Data import fetch_data_by_condition
import folium

def geo_fencing(latitude_range, longitude_range, db_name="gps_data.db"):
    """
    Check if any vehicle is outside the defined geo-fence and visualize on a map.
    :param latitude_range: Tuple (min_lat, max_lat) defining latitude bounds
    :param longitude_range: Tuple (min_lon, max_lon) defining longitude bounds
    :param db_name: Name of the SQLite database file
    :return: List of vehicles outside the geo-fence
    """
    min_lat, max_lat = latitude_range
    min_lon, max_lon = longitude_range
    condition = f"latitude < {min_lat} OR latitude > {max_lat} OR longitude < {min_lon} OR longitude > {max_lon}"
    outside_data = fetch_data_by_condition(condition, db_name)
    
    # Create a map centered around the average location
    map_center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
    map_ = folium.Map(location=map_center, zoom_start=12)

    # Highlight the geo-fenced area
    folium.Rectangle(
        bounds=[[min_lat, min_lon], [max_lat, max_lon]],
        color='blue',
        fill=True,
        fill_opacity=0.2,
        popup='Geo-fenced Area'
    ).add_to(map_)

    if outside_data.empty:
        print("No vehicles outside the geo-fenced area.")
        return []
    else:
        print("Vehicles outside the geo-fenced area:")
        print(outside_data)
        
        # Plot vehicles outside the geo-fence on the map
        for _, row in outside_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Tracker ID: {row['tracker_id']}, Speed: {row['speed']} km/h",
                icon=folium.Icon(color='red')
            ).add_to(map_)
        
        # Save the map to an HTML file
        map_.save("geo_fencing_map.html")
        print("Map has been saved as 'geo_fencing_map.html'.")
        
        return outside_data.to_dict('records')

# Example usage
geo_fence_violations = geo_fencing((28.5, 28.7), (77.0, 77.2))
