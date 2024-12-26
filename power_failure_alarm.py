from realtime_Data import fetch_data_by_condition
def power_failure_alarm(db_name="gps_data.db"):
    """
    Check for vehicles where the power status is 'Off'.
    :param db_name: Name of the SQLite database file
    :return: List of vehicles with power failure
    """
    condition = "power_status = 'Off'"
    power_failure_data = fetch_data_by_condition(condition, db_name)
    if power_failure_data.empty:
        print("No power failures detected.")
        return []
    else:
        print("Power failures detected:")
        print(power_failure_data)
        return power_failure_data.to_dict('records')

# Example usage
power_failures = power_failure_alarm()
