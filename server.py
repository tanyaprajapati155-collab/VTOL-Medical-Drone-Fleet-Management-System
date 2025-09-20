"""
Flask Server for VTOL Medical Drone System
Replaces Streamlit with a local Flask server
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import random
import threading
import time

# Import our existing data managers
from drone_data import DroneDataManager
from medical_supplies import MedicalSupplyManager
from utils.alerts import AlertManager
from utils.authentication import authenticate_user

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize data managers
drone_manager = DroneDataManager()
medical_manager = MedicalSupplyManager()
alert_manager = AlertManager()

# Global state for real-time updates
app_data = {
    'drone_fleet': [],
    'medical_supplies': [],
    'kpi_data': {
        'total_drones': 15,
        'active_missions': 8,
        'success_rate': 94.5,
        'avg_delivery_time': 12.3
    },
    'alerts': [],
    'activities': []
}

def update_app_data():
    """Update application data from managers"""
    # Update drone fleet data
    fleet_status = drone_manager.get_detailed_fleet_status()
    app_data['drone_fleet'] = fleet_status
    
    # Update medical supplies data
    inventory_df = medical_manager.inventory
    app_data['medical_supplies'] = inventory_df.to_dict('records')
    
    # Update KPI data
    fleet_overview = drone_manager.get_fleet_overview()
    mission_stats = drone_manager.get_mission_stats()
    inventory_overview = medical_manager.get_inventory_overview()
    
    app_data['kpi_data'] = {
        'total_drones': fleet_overview['total'],
        'active_missions': fleet_overview['active'],
        'success_rate': mission_stats['success_rate'],
        'avg_delivery_time': mission_stats['avg_delivery_time']
    }
    
    # Update alerts
    app_data['alerts'] = alert_manager.get_active_alerts()
    
    # Update activities
    app_data['activities'] = alert_manager.get_recent_activities()

def simulate_real_time_updates():
    """Simulate real-time data updates"""
    while True:
        # Update drone data
        drone_manager.simulate_real_time_data()
        
        # Update application data
        update_app_data()
        
        # Sleep for 5 seconds
        time.sleep(5)

# Start real-time simulation in background thread
update_thread = threading.Thread(target=simulate_real_time_updates, daemon=True)
update_thread.start()

# Serve static files
@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

# API Endpoints

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user authentication"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if authenticate_user(username, password):
        return jsonify({
            'success': True,
            'user': {
                'username': username,
                'role': 'Administrator',  # Simplified for demo
                'full_name': f'{username.title()} User'
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/dashboard/kpis')
def get_kpis():
    """Get key performance indicators"""
    return jsonify(app_data['kpi_data'])

@app.route('/api/fleet/overview')
def get_fleet_overview():
    """Get fleet overview data"""
    fleet_overview = drone_manager.get_fleet_overview()
    return jsonify(fleet_overview)

@app.route('/api/fleet/status')
def get_fleet_status():
    """Get detailed fleet status"""
    return jsonify(app_data['drone_fleet'])

@app.route('/api/fleet/<drone_id>')
def get_drone_details(drone_id):
    """Get details for a specific drone"""
    drone_details = drone_manager.get_drone_details(drone_id)
    if drone_details:
        return jsonify(drone_details)
    else:
        return jsonify({'error': 'Drone not found'}), 404

@app.route('/api/fleet/<drone_id>/status', methods=['PUT'])
def update_drone_status(drone_id):
    """Update drone status"""
    data = request.get_json()
    new_status = data.get('status')
    
    if drone_manager.update_drone_status(drone_id, new_status):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to update status'}), 400

@app.route('/api/fleet/<drone_id>/deploy', methods=['POST'])
def deploy_drone(drone_id):
    """Deploy a drone on a mission"""
    data = request.get_json()
    mission_type = data.get('mission_type')
    destination = data.get('destination')
    priority = data.get('priority', 'Medium')
    
    if drone_manager.deploy_drone(drone_id, mission_type, destination, priority):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to deploy drone'}), 400

@app.route('/api/fleet/<drone_id>/recall', methods=['POST'])
def recall_drone(drone_id):
    """Recall a drone back to base"""
    if drone_manager.recall_drone(drone_id):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to recall drone'}), 400

@app.route('/api/analytics/success-rate')
def get_success_rate():
    """Get mission success rate"""
    success_rate = drone_manager.get_success_rate()
    return jsonify({'success_rate': success_rate})

@app.route('/api/analytics/delivery-trends')
def get_delivery_trends():
    """Get delivery time trends"""
    trends = drone_manager.get_delivery_trends()
    return jsonify(trends.to_dict('records'))

@app.route('/api/analytics/mission-distribution')
def get_mission_distribution():
    """Get mission type distribution"""
    distribution = drone_manager.get_mission_distribution()
    return jsonify(distribution)

@app.route('/api/analytics/battery-distribution')
def get_battery_distribution():
    """Get battery level distribution"""
    distribution = drone_manager.get_battery_distribution()
    return jsonify(distribution)

@app.route('/api/medical/inventory')
def get_medical_inventory():
    """Get medical inventory data"""
    return jsonify(app_data['medical_supplies'])

@app.route('/api/medical/inventory/overview')
def get_medical_overview():
    """Get medical inventory overview"""
    overview = medical_manager.get_inventory_overview()
    return jsonify(overview)

@app.route('/api/medical/inventory/critical-alerts')
def get_medical_alerts():
    """Get critical medical inventory alerts"""
    alerts = medical_manager.get_critical_alerts()
    return jsonify(alerts)

@app.route('/api/medical/deliveries')
def get_active_deliveries():
    """Get active medical deliveries"""
    deliveries = medical_manager.get_active_deliveries()
    return jsonify(deliveries)

@app.route('/api/medical/deliveries', methods=['POST'])
def create_delivery():
    """Create a new medical delivery"""
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    destination = data.get('destination')
    priority = data.get('priority', 'Medium')
    drone_id = data.get('drone_id')
    
    delivery = medical_manager.create_delivery_order(
        item_id, quantity, destination, priority, drone_id
    )
    
    if delivery:
        return jsonify(delivery)
    else:
        return jsonify({'error': 'Failed to create delivery'}), 400

@app.route('/api/alerts')
def get_alerts():
    """Get active alerts"""
    return jsonify(app_data['alerts'])

@app.route('/api/alerts/emergency', methods=['POST'])
def create_emergency_alert():
    """Create an emergency alert"""
    alert_manager.create_emergency_alert()
    return jsonify({'success': True})

@app.route('/api/activities')
def get_activities():
    """Get recent activities"""
    return jsonify(app_data['activities'])

@app.route('/api/system/health')
def get_system_health():
    """Get system health status"""
    health = {
        "Drone Fleet": "OK",
        "GPS Tracking": "OK", 
        "Communication": "OK",
        "Medical Inventory": "OK",
        "Weather Service": "OK",
        "Database": "OK"
    }
    return jsonify(health)

@app.route('/api/mission/stats')
def get_mission_stats():
    """Get mission statistics"""
    stats = drone_manager.get_mission_stats()
    return jsonify(stats)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize data
    update_app_data()
    
    PORT = 8080  # Use port 8080 instead of 5000 to avoid macOS AirPlay conflict
    
    print("🚁 VTOL Medical Drone System Server Starting...")
    print(f"📡 API Endpoints available at http://localhost:{PORT}/api/")
    print(f"🌐 Web Interface available at http://localhost:{PORT}/")
    print("🔧 Real-time updates enabled")
    
    app.run(debug=True, host='0.0.0.0', port=PORT)
