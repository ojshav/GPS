from realtime_Data import fetch_data_by_condition
def speed_alarm(speed_limit=80, tracker_id=None, db_name="gps_data.db"):
    """
    Check for vehicles exceeding the speed limit and return their details.
    :param speed_limit: Speed limit in km/h
    :param tracker_id: Optional tracker ID to filter by vehicle
    :param db_name: Name of the SQLite database file
    :return: List of vehicles exceeding the speed limit
    """
    if tracker_id:
        condition = f"speed > {speed_limit} AND tracker_id = '{tracker_id}'"
    else:
        condition = f"speed > {speed_limit}"
    
    high_speed_data = fetch_data_by_condition(condition, db_name)
    if high_speed_data.empty:
        print(f"No vehicles exceeding the speed limit of {speed_limit} km/h.")
        return []
    else:
        print(f"Vehicles exceeding the speed limit of {speed_limit} km/h:")
        print(high_speed_data)
        return high_speed_data.to_dict('records')

# Example usage
violations = speed_alarm(speed_limit=80, tracker_id="TRACKER_1000")
