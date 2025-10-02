"""
Medical Supply Management Utilities
Handles inventory tracking, delivery management, and supply chain operations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

class MedicalSupplyManager:
    """Main class for managing medical supply inventory and deliveries"""

    def __init__(self):
        self.inventory = self._initialize_inventory()
        self.active_deliveries = []
        self.delivery_history = []
        self.temperature_monitors = {}

    def _initialize_inventory(self):
        """Initialize medical supply inventory"""

        # Define medical supply categories and items
        medical_categories = {
            'Blood Products': [
                'O+ Blood Pack', 'O- Blood Pack', 'A+ Blood Pack', 'A- Blood Pack', 
                'B+ Blood Pack', 'B- Blood Pack', 'AB+ Blood Pack', 'AB- Blood Pack',
                'Platelet Concentrate', 'Fresh Frozen Plasma'
            ],
            'Emergency Medications': [
                'Epinephrine Auto-Injector', 'Morphine Sulfate', 'Atropine Sulfate',
                'Naloxone (Narcan)', 'Adenosine', 'Amiodarone', 'Dopamine',
                'Norepinephrine', 'Lidocaine', 'Diazepam'
            ],
            'IV Fluids & Solutions': [
                'Normal Saline (0.9%)', 'Lactated Ringers', 'D5W (5% Dextrose)',
                'D5NS', 'Half Normal Saline', 'Plasma Expander', 'Albumin 5%',
                'Mannitol', 'Hypertonic Saline'
            ],
            'Surgical & Trauma Supplies': [
                'Trauma Surgery Kit', 'Emergency Suture Kit', 'Chest Tube Kit',
                'Emergency Airway Kit', 'Burn Treatment Kit', 'Hemostatic Agents',
                'Emergency Thoracotomy Kit', 'Vascular Access Kit'
            ],
            'Vaccines & Biologics': [
                'COVID-19 Vaccine', 'Hepatitis B Vaccine', 'Tetanus Toxoid',
                'Rabies Vaccine', 'Influenza Vaccine', 'Immunoglobulin',
                'Anti-Venom Serum', 'Botulism Antitoxin'
            ],
            'Medical Equipment': [
                'Portable Defibrillator', 'Oxygen Tank (Portable)', 'Blood Glucose Monitor',
                'Digital Thermometer', 'Pulse Oximeter', 'Blood Pressure Cuff',
                'Portable Ventilator', 'Emergency Surgical Tools'
            ],
            'Diagnostic Supplies': [
                'Rapid COVID Test', 'Blood Test Strips', 'Pregnancy Test',
                'Drug Screen Kit', 'Malaria Test Kit', 'Cardiac Biomarker Test',
                'Hemoglobin Test Kit', 'Infection Marker Test'
            ]
        }

        inventory_data = []
        item_id_counter = 1

        for category, items in medical_categories.items():
            for item in items:
                # Determine temperature requirements based on item type
                if 'Blood' in item or 'Vaccine' in item or 'Plasma' in item:
                    temp_req = '2-8°C'
                elif 'Frozen' in item or 'Anti-Venom' in item:
                    temp_req = '-20°C'
                else:
                    temp_req = 'Room Temp'

                # Set priority based on item criticality
                if any(word in item.lower() for word in ['blood', 'epinephrine', 'trauma', 'emergency']):
                    priority = 'Critical'
                elif any(word in item.lower() for word in ['vaccine', 'antitoxin', 'surgical']):
                    priority = 'High'
                else:
                    priority = random.choice(['Medium', 'Low'])

                inventory_data.append({
                    'item_id': f"MED-{item_id_counter:04d}",
                    'category': category,
                    'item_name': item,
                    'current_stock': random.randint(5, 150),
                    'min_stock_level': random.randint(10, 30),
                    'max_stock_level': random.randint(100, 200),
                    'unit_of_measure': random.choice(['units', 'vials', 'packs', 'doses', 'kits']),
                    'temperature_requirement': temp_req,
                    'expiry_date': datetime.now() + timedelta(days=random.randint(30, 1095)),
                    'batch_number': f"BT{random.randint(10000, 99999)}",
                    'supplier': random.choice(['MedSupply Corp', 'HealthTech Ltd', 'BioMed Solutions', 'PharmaCare Inc']),
                    'unit_cost': random.uniform(5, 500),
                    'location': f"Cold Storage {random.choice(['A', 'B', 'C'])}" if temp_req != 'Room Temp' else f"Storage Unit {random.choice(['D', 'E', 'F'])}",
                    'priority': priority,
                    'last_restocked': datetime.now() - timedelta(days=random.randint(1, 60)),
                    'reserved_stock': random.randint(0, 10),
                    'quality_status': random.choice(['Good', 'Good', 'Good', 'Warning'])  # 75% good quality
                })

                item_id_counter += 1

        return pd.DataFrame(inventory_data)

    def get_inventory_overview(self):
        """Get high-level inventory statistics"""
        total_items = len(self.inventory)

        # Calculate availability percentage
        available_items = len(self.inventory[self.inventory['current_stock'] > self.inventory['min_stock_level']])
        availability_percent = (available_items / total_items) * 100

        # Critical stock items
        critical_stock = len(self.inventory[self.inventory['current_stock'] <= self.inventory['min_stock_level']])

        return {
            'total_items': total_items,
            'availability': availability_percent,
            'critical_stock': critical_stock,
            'change': random.uniform(-5, 10),  # Simulated change
            'total_value': (self.inventory['current_stock'] * self.inventory['unit_cost']).sum()
        }

    def get_critical_alerts(self):
        """Get list of critical inventory alerts"""
        alerts = []

        # Low stock alerts
        low_stock = self.inventory[self.inventory['current_stock'] <= self.inventory['min_stock_level']]
        for _, item in low_stock.iterrows():
            alerts.append({
                'type': 'Low Stock',
                'severity': 'Critical' if item['current_stock'] < item['min_stock_level'] * 0.5 else 'Warning',
                'item': item['item_name'],
                'current_stock': item['current_stock'],
                'min_required': item['min_stock_level'],
                'category': item['category']
            })

        # Expiring items (within 30 days)
        expiring_soon = self.inventory[
            (self.inventory['expiry_date'] - datetime.now()).dt.days <= 30
        ]
        for _, item in expiring_soon.iterrows():
            days_to_expiry = (item['expiry_date'] - datetime.now()).days
            alerts.append({
                'type': 'Expiring Soon',
                'severity': 'Critical' if days_to_expiry <= 7 else 'Warning',
                'item': item['item_name'],
                'days_remaining': days_to_expiry,
                'batch_number': item['batch_number'],
                'quantity': item['current_stock']
            })

        # Temperature alerts (simulated)
        temp_alerts = random.randint(0, 2)
        for i in range(temp_alerts):
            alerts.append({
                'type': 'Temperature Alert',
                'severity': 'Warning',
                'item': 'Cold Storage Unit',
                'message': f"Temperature fluctuation detected in {random.choice(['Storage A', 'Storage B', 'Storage C'])}"
            })

        return alerts

    def create_delivery_order(self, item_id, quantity, destination, priority='Medium', drone_id=None):
        """Create a new delivery order"""

        # Find the item in inventory
        item_row = self.inventory[self.inventory['item_id'] == item_id]
        if item_row.empty:
            return None

        item = item_row.iloc[0]

        # Check if sufficient stock available
        available_stock = item['current_stock'] - item['reserved_stock']
        if available_stock < quantity:
            return None

        # Create delivery order
        delivery_id = f"DEL-{len(self.active_deliveries) + len(self.delivery_history) + 1:06d}"

        delivery_order = {
            'delivery_id': delivery_id,
            'item_id': item_id,
            'item_name': item['item_name'],
            'category': item['category'],
            'quantity': quantity,
            'unit_of_measure': item['unit_of_measure'],
            'destination': destination,
            'priority': priority,
            'drone_id': drone_id,
            'status': 'Pending' if drone_id is None else 'Assigned',
            'created_time': datetime.now(),
            'estimated_delivery_time': datetime.now() + timedelta(minutes=random.randint(15, 45)),
            'temperature_requirement': item['temperature_requirement'],
            'special_handling': self._get_special_handling_requirements(item),
            'batch_number': item['batch_number'],
            'chain_of_custody': [],
            'temperature_log': []
        }

        # Reserve the stock
        self.inventory.loc[self.inventory['item_id'] == item_id, 'reserved_stock'] += quantity

        # Add to active deliveries
        self.active_deliveries.append(delivery_order)

        return delivery_order

    def update_delivery_status(self, delivery_id, new_status, location=None, temperature=None):
        """Update the status of a delivery"""

        for delivery in self.active_deliveries:
            if delivery['delivery_id'] == delivery_id:
                delivery['status'] = new_status

                # Add chain of custody entry
                custody_entry = {
                    'timestamp': datetime.now(),
                    'status': new_status,
                    'location': location,
                    'temperature': temperature
                }
                delivery['chain_of_custody'].append(custody_entry)

                # If delivery completed, move to history and update inventory
                if new_status == 'Delivered':
                    self._complete_delivery(delivery)
                    # Ensure status is set before moving to history
                    delivery['status'] = 'Delivered'
                    self.active_deliveries.remove(delivery)
                    self.delivery_history.append(delivery)

                return True

        return False

    def get_active_deliveries(self):
        """Get list of all active deliveries"""
        return self.active_deliveries

    def get_delivery_history(self, days=7):
        """Get delivery history for specified number of days"""
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_deliveries = [
            delivery for delivery in self.delivery_history
            if delivery['created_time'] >= cutoff_date
        ]

        return recent_deliveries

    def get_temperature_alerts(self):
        """Get temperature monitoring alerts"""
        alerts = []

        # Simulate temperature monitoring
        for delivery in self.active_deliveries:
            if delivery['temperature_requirement'] != 'Room Temp':
                # Simulate temperature readings
                if random.random() < 0.1:  # 10% chance of temperature alert
                    alerts.append({
                        'delivery_id': delivery['delivery_id'],
                        'item_name': delivery['item_name'],
                        'required_temp': delivery['temperature_requirement'],
                        'current_temp': f"{random.uniform(-2, 12):.1f}°C",
                        'alert_type': 'Temperature Deviation',
                        'severity': 'Warning'
                    })

        return alerts

    def get_inventory_by_category(self):
        """Get inventory summary by category"""
        category_summary = self.inventory.groupby('category').agg({
            'current_stock': 'sum',
            'unit_cost': lambda x: (self.inventory.loc[x.index, 'current_stock'] * x).sum(),
            'item_id': 'count'
        }).round(2)

        category_summary.columns = ['Total_Stock', 'Total_Value', 'Item_Count']
        return category_summary.reset_index()

    def search_inventory(self, search_term):
        """Search inventory by item name or category"""
        mask = (
            self.inventory['item_name'].str.contains(search_term, case=False, na=False) |
            self.inventory['category'].str.contains(search_term, case=False, na=False)
        )
        return self.inventory[mask]

    def _get_special_handling_requirements(self, item):
        """Determine special handling requirements for an item"""
        special_handling = []

        if item['temperature_requirement'] != 'Room Temp':
            special_handling.append('Temperature Controlled')

        if 'Blood' in item['item_name']:
            special_handling.append('Biohazard')
            special_handling.append('Urgent Delivery')

        if item['priority'] == 'Critical':
            special_handling.append('Priority Handling')

        if 'Vaccine' in item['item_name']:
            special_handling.append('Cold Chain Required')

        return special_handling

    def _complete_delivery(self, delivery):
        """Complete a delivery and update inventory"""
        # Reduce reserved stock and actual stock
        item_id = delivery['item_id']
        quantity = delivery['quantity']

        mask = self.inventory['item_id'] == item_id
        self.inventory.loc[mask, 'reserved_stock'] -= quantity
        self.inventory.loc[mask, 'current_stock'] -= quantity

        # Add completion timestamp
        delivery['completed_time'] = datetime.now()
        delivery['actual_delivery_time'] = delivery['completed_time']

    def restock_item(self, item_id, quantity, batch_number=None, expiry_date=None):
        """Restock an inventory item"""
        mask = self.inventory['item_id'] == item_id

        if not self.inventory[mask].empty:
            self.inventory.loc[mask, 'current_stock'] += quantity
            self.inventory.loc[mask, 'last_restocked'] = datetime.now()

            if batch_number:
                self.inventory.loc[mask, 'batch_number'] = batch_number

            if expiry_date:
                self.inventory.loc[mask, 'expiry_date'] = expiry_date

            return True

        return False

    def get_supply_chain_metrics(self):
        """Get supply chain performance metrics"""

        # Calculate delivery performance
        if self.delivery_history:
            completed_deliveries = [d for d in self.delivery_history if d['status'] == 'Delivered']

            if completed_deliveries:
                # Average delivery time
                avg_delivery_time = np.mean([
                    (d['actual_delivery_time'] - d['created_time']).total_seconds() / 60
                    for d in completed_deliveries
                ])

                # On-time delivery rate
                on_time_deliveries = sum(
                    1 for d in completed_deliveries
                    if d['actual_delivery_time'] <= d['estimated_delivery_time']
                )
                on_time_rate = (on_time_deliveries / len(completed_deliveries)) * 100
            else:
                avg_delivery_time = 0
                on_time_rate = 0
        else:
            avg_delivery_time = 0
            on_time_rate = 0

        return {
            'avg_delivery_time_minutes': avg_delivery_time,
            'on_time_delivery_rate': on_time_rate,
            'active_deliveries': len(self.active_deliveries),
            'completed_deliveries_7d': len([
                d for d in self.delivery_history
                if (datetime.now() - d['created_time']).days <= 7
            ])
        }

# Helper functions
def calculate_storage_requirements(inventory_df):
    """Calculate storage space requirements by temperature"""
    storage_req = inventory_df.groupby('temperature_requirement').agg({
        'current_stock': 'sum',
        'item_name': 'count'
    })
    return storage_req

def generate_supply_forecast(inventory_df, days=30):
    """Generate supply requirement forecast"""
    forecast = {}

    for _, item in inventory_df.iterrows():
        # Simple forecast based on current consumption rate
        daily_usage = random.uniform(0.5, 3.0)  # Simulated daily usage
        days_remaining = item['current_stock'] / daily_usage

        if days_remaining < days:
            shortage_date = datetime.now() + timedelta(days=days_remaining)
            forecast[item['item_name']] = {
                'current_stock': item['current_stock'],
                'daily_usage': daily_usage,
                'shortage_date': shortage_date,
                'recommended_reorder': item['max_stock_level'] - item['current_stock']
            }

    return forecast
