"""
Drone Data Management Utilities
Handles real-time drone data, fleet management, and mission tracking
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

class DroneDataManager:
    """Main class for managing drone fleet data and operations"""

    def __init__(self):
        self.drone_count = 15
        self.drones = self._initialize_fleet()
        self.mission_history = []
        self.last_update = datetime.now()

    def _initialize_fleet(self):
        """Initialize the drone fleet with default values"""
        drone_fleet = {}

        for i in range(1, self.drone_count + 1):
            drone_id = f"LLA-{i:03d}"

            # Base coordinates (Delhi area for example)
            base_lat, base_lon = 28.6139, 77.2090

            drone_fleet[drone_id] = {
                'id': drone_id,
                'status': random.choice(['Active', 'Charging', 'Maintenance', 'Standby']),
                'battery': random.randint(20, 100),
                'location': {
                    'lat': base_lat + random.uniform(-0.05, 0.05),
                    'lon': base_lon + random.uniform(-0.05, 0.05),
                    'altitude': random.uniform(0, 150),
                    'zone': random.choice(['Zone Alpha', 'Zone Beta', 'Zone Gamma', 'Base Station'])
                },
                'mission': {
                    'type': random.choice(['Medical Delivery', 'Search & Rescue', 'Supply Drop', 'Reconnaissance', 'Standby']),
                    'destination': f'Station {chr(65 + random.randint(0, 4))}',
                    'start_time': datetime.now() - timedelta(minutes=random.randint(0, 120)),
                    'estimated_duration': random.randint(15, 60),
                    'priority': random.choice(['Critical', 'High', 'Medium', 'Low'])
                },
                'technical': {
                    'model': 'VTOL-MD-2024',
                    'max_range': 25,  # km
                    'max_payload': 5,  # kg
                    'max_speed': 80,  # km/h
                    'current_speed': random.uniform(0, 80) if random.choice(['Active']) else 0,
                    'flight_time_total': random.uniform(100, 800),  # hours
                    'cycles_total': random.randint(500, 2000)
                },
                'last_update': datetime.now() - timedelta(minutes=random.randint(0, 5))
            }

        return drone_fleet

    def get_fleet_overview(self):
        """Get high-level fleet statistics"""
        active_count = len([d for d in self.drones.values() if d['status'] == 'Active'])
        charging_count = len([d for d in self.drones.values() if d['status'] == 'Charging'])
        maintenance_count = len([d for d in self.drones.values() if d['status'] == 'Maintenance'])

        return {
            'total': len(self.drones),
            'active': active_count,
            'charging': charging_count,
            'maintenance': maintenance_count,
            'change': random.randint(-2, 5),  # Simulated change from previous period
            'active_change': random.randint(-1, 3)
        }

    def get_detailed_fleet_status(self):
        """Get detailed status for all drones"""
        fleet_status = []

        for drone_id, drone in self.drones.items():
            fleet_status.append({
                'id': drone['id'],
                'status': drone['status'],
                'battery': drone['battery'],
                'mission': drone['mission']['type'],
                'location': drone['location']['zone'],
                'lat': drone['location']['lat'],
                'lon': drone['location']['lon'],
                'altitude': drone['location']['altitude'],
                'speed': drone['technical']['current_speed'],
                'last_update': drone['last_update']
            })

        return fleet_status

    def get_drone_details(self, drone_id):
        """Get detailed information for a specific drone"""
        if drone_id in self.drones:
            return self.drones[drone_id]
        return None

    def update_drone_status(self, drone_id, new_status):
        """Update the status of a specific drone"""
        if drone_id in self.drones:
            self.drones[drone_id]['status'] = new_status
            self.drones[drone_id]['last_update'] = datetime.now()

            # Log the status change
            self._log_status_change(drone_id, new_status)
            return True
        return False

    def simulate_real_time_data(self):
        """Simulate real-time updates to drone data"""
        for drone_id, drone in self.drones.items():
            # Simulate battery drain for active drones
            if drone['status'] == 'Active':
                battery_drain = random.uniform(0.5, 2.0)
                drone['battery'] = max(0, drone['battery'] - battery_drain)

                # Force return if battery too low
                if drone['battery'] < 15:
                    drone['status'] = 'Returning'
                    drone['mission']['type'] = 'Return to Base'

            # Simulate battery charging
            elif drone['status'] == 'Charging':
                charge_rate = random.uniform(1.0, 3.0)
                drone['battery'] = min(100, drone['battery'] + charge_rate)

                # Ready for deployment when fully charged
                if drone['battery'] >= 95:
                    drone['status'] = 'Standby'

            # Update location for active drones
            if drone['status'] in ['Active', 'Returning']:
                # Simulate movement
                lat_change = random.uniform(-0.001, 0.001)
                lon_change = random.uniform(-0.001, 0.001)
                drone['location']['lat'] += lat_change
                drone['location']['lon'] += lon_change

                # Update speed
                drone['technical']['current_speed'] = random.uniform(30, 80)
            else:
                drone['technical']['current_speed'] = 0

            # Update last update timestamp
            drone['last_update'] = datetime.now()

    def get_mission_stats(self):
        """Get mission performance statistics"""
        # Simulate mission data
        today_missions = random.randint(15, 35)
        yesterday_missions = random.randint(10, 30)

        return {
            'completed_today': today_missions,
            'change_percent': ((today_missions - yesterday_missions) / yesterday_missions) * 100,
            'avg_delivery_time': random.uniform(8, 15),
            'delivery_time_change': random.uniform(-2, 1),
            'success_rate': random.uniform(92, 98)
        }

    def get_success_rate(self):
        """Get current mission success rate"""
        return random.uniform(92, 98)

    def get_delivery_trends(self):
        """Get delivery time trends over the past week"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')

        trend_data = []
        for date in dates:
            trend_data.append({
                'date': date,
                'avg_delivery_time': random.uniform(8, 16),
                'missions_completed': random.randint(8, 25)
            })

        return pd.DataFrame(trend_data)

    def get_mission_distribution(self):
        """Get distribution of mission types"""
        return {
            'Medical Delivery': 65,
            'Search & Rescue': 15,
            'Supply Drop': 12,
            'Reconnaissance': 5,
            'Emergency Response': 3
        }

    def get_battery_distribution(self):
        """Get battery level distribution across fleet"""
        battery_ranges = {
            '80-100%': 0,
            '60-80%': 0,
            '40-60%': 0,
            '20-40%': 0,
            '0-20%': 0
        }

        for drone in self.drones.values():
            battery = drone['battery']
            if battery >= 80:
                battery_ranges['80-100%'] += 1
            elif battery >= 60:
                battery_ranges['60-80%'] += 1
            elif battery >= 40:
                battery_ranges['40-60%'] += 1
            elif battery >= 20:
                battery_ranges['20-40%'] += 1
            else:
                battery_ranges['0-20%'] += 1

        return battery_ranges

    def get_average_battery(self):
        """Get average battery level across fleet"""
        total_battery = sum(drone['battery'] for drone in self.drones.values())
        return total_battery / len(self.drones)

    def deploy_drone(self, drone_id, mission_type, destination, priority='Medium'):
        """Deploy a drone on a new mission"""
        if drone_id in self.drones and self.drones[drone_id]['status'] == 'Standby':
            drone = self.drones[drone_id]
            drone['status'] = 'Active'
            drone['mission'] = {
                'type': mission_type,
                'destination': destination,
                'start_time': datetime.now(),
                'estimated_duration': random.randint(15, 60),
                'priority': priority
            }
            drone['last_update'] = datetime.now()

            self._log_mission_start(drone_id, mission_type, destination)
            return True
        return False

    def recall_drone(self, drone_id):
        """Recall a drone back to base"""
        if drone_id in self.drones and self.drones[drone_id]['status'] == 'Active':
            drone = self.drones[drone_id]
            drone['status'] = 'Returning'
            drone['mission']['type'] = 'Return to Base'
            drone['last_update'] = datetime.now()

            self._log_status_change(drone_id, 'Returning')
            return True
        return False

    def _log_status_change(self, drone_id, new_status):
        """Log status changes for audit trail"""
        log_entry = {
            'timestamp': datetime.now(),
            'drone_id': drone_id,
            'event_type': 'status_change',
            'new_status': new_status
        }
        # In a real implementation, this would write to a database
        print(f"LOG: {drone_id} status changed to {new_status}")

    def _log_mission_start(self, drone_id, mission_type, destination):
        """Log mission start for tracking"""
        log_entry = {
            'timestamp': datetime.now(),
            'drone_id': drone_id,
            'event_type': 'mission_start',
            'mission_type': mission_type,
            'destination': destination
        }
        self.mission_history.append(log_entry)
        print(f"LOG: {drone_id} started {mission_type} mission to {destination}")

    def get_flight_hours_total(self):
        """Get total flight hours across all drones"""
        return sum(drone['technical']['flight_time_total'] for drone in self.drones.values())

    def get_emergency_drones(self):
        """Get list of drones available for emergency deployment"""
        emergency_ready = []
        for drone_id, drone in self.drones.items():
            if (drone['status'] == 'Standby' and 
                drone['battery'] > 80):
                emergency_ready.append(drone_id)
        return emergency_ready

# Helper functions for coordinates and mapping
def get_drone_coordinates(drone_id):
    """Get GPS coordinates for a specific drone"""
    # Base coordinates with some variation
    base_lat, base_lon = 28.6139, 77.2090

    # Add some randomization for demonstration
    lat = base_lat + np.random.uniform(-0.05, 0.05)
    lon = base_lon + np.random.uniform(-0.05, 0.05)

    return lat, lon

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates"""
    from math import radians, cos, sin, asin, sqrt

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers

    return c * r

def estimate_flight_time(distance_km, speed_kmh=60):
    """Estimate flight time based on distance and speed"""
    return (distance_km / speed_kmh) * 60  # Return in minutes
