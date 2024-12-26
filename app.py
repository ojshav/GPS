from flask import Flask, render_template, request
from immobilize import immobilize_vehicle
from point_of_interest import point_of_interest_mapping, visualize_pois
from displacement_alarm import displacement_alarm
from spped_alarm_module import speed_alarm
from power_failure_alarm import power_failure_alarm
from geofencing import geo_fencing


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/immobilize', methods=['POST'])
def immobilize():
    tracker_id = request.form['tracker_id']
    message = immobilize_vehicle(tracker_id)
    return render_template('index.html', message=message)

@app.route('/poi', methods=['POST'])
def poi():
    """
    Handles the Point of Interest mapping and visualization.
    """
    try:
        location = request.form.get('location')  # Get location input from the form
        radius_km = float(request.form.get('radius', 100))  # Default radius is 0.5 km
        db_name = "gps_data.db"  # Name of the SQLite database file

        # Sample POIs, these could also be dynamically fetched based on `location`
        pois = [
            (28.6139, 77.2090, "India Gate"),
            (28.7041, 77.1025, "Connaught Place"),
        ]

        # Extract (lat, lon) tuples for mapping
        poi_locations = [(poi[0], poi[1]) for poi in pois]

        # Find vehicles near POIs
        nearby_vehicles = point_of_interest_mapping(poi_locations, radius_km=radius_km, db_name=db_name)

        # Visualize POIs on a map
        map_name = "pois_map.html"
        visualize_pois(pois, map_name=map_name)

        # Render results
        return render_template('poi_results.html', nearby_vehicles=nearby_vehicles, map_file=map_name)
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {e}")



@app.route('/displacement', methods=['POST'])
def displacement():
    # Call the updated displacement_alarm function to get alerts
    alerts = displacement_alarm(threshold_km=1)  # Adjust threshold as needed
    
    # Prepare data for rendering
    results = []
    for alert in alerts:
        results.append({
            'tracker_id': alert['tracker_id'],
            'previous_address': alert['previous_address'],
            'current_address': alert['current_address'],
            'distance_km': alert['displacement_km'],
            'prev_location': alert['prev_location'],
            'current_location': alert['current_location'],
        })
    
    return render_template('displacement.html', results=results)

@app.route('/speed_alarm', methods=['POST'])
def speed_alarm_route():
    speed_limit = request.form['speed_limit']
    violations = speed_alarm(speed_limit=speed_limit)
    return render_template('index.html', violations=violations)

@app.route('/power_failure', methods=['POST'])
def power_failure():
    power_failures = power_failure_alarm()
    return render_template('index.html', power_failures=power_failures)

@app.route('/geofencing', methods=['POST'])
def geofencing():
    latitude_range = (28.5, 28.7)
    longitude_range = (77.0, 77.2)
    geo_fence_violations = geo_fencing(latitude_range, longitude_range)
    
    # Prepare data for rendering
    violations_data = [
        {
            "id": violation['id'],
            "tracker_id": violation['tracker_id'],
            "latitude": violation['latitude'],
            "longitude": violation['longitude'],
            "speed": violation['speed'],
            "status": violation['status'],
            "power_status": violation['power_status'],
            "timestamp": violation['timestamp']
        } for violation in geo_fence_violations
    ]
    
    return render_template('geo_fencing_map.html', geo_fence_violations=violations_data)

if __name__ == '__main__':
    app.run(debug=True)
