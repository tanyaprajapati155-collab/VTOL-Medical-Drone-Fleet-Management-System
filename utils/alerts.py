"""
Advanced Alert Management System
Real-time monitoring and notification system for VTOL medical drone operations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from typing import Dict, List, Optional

class AlertManager:
    """Comprehensive alert management system"""

    def __init__(self):
        self.active_alerts = []
        self.alert_history = []
        self.recent_activities = []
        self.alert_thresholds = {
            'battery_critical': 15,
            'battery_low': 25,
            'stock_critical': 5,
            'stock_low': 15,
            'temperature_deviation': 2.0
        }

    def create_alert(self, alert_type: str, severity: str, title: str, message: str, 
                    source: str = "System", metadata: Optional[Dict] = None):
        """Create a new alert with comprehensive details"""
        alert = {
            'id': f"ALT-{len(self.active_alerts) + len(self.alert_history) + 1:06d}",
            'type': alert_type,
            'severity': severity,
            'title': title,
            'message': message,
            'source': source,
            'timestamp': datetime.now(),
            'location': metadata.get('location', 'System') if metadata else 'System',
            'acknowledged': False,
            'resolved': False,
            'metadata': metadata or {},
            'priority_score': self._calculate_priority_score(severity, alert_type)
        }

        self.active_alerts.append(alert)
        self._log_activity(f"Alert created: {title}", "alert")
        return alert

    def _calculate_priority_score(self, severity: str, alert_type: str) -> int:
        """Calculate priority score for alert ordering"""
        severity_scores = {'critical': 100, 'warning': 50, 'info': 20, 'success': 10}
        type_multipliers = {
            'drone_battery': 1.5,
            'medical_supply': 1.3,
            'system_error': 1.4,
            'weather': 1.1,
            'maintenance': 1.0
        }

        base_score = severity_scores.get(severity, 0)
        multiplier = type_multipliers.get(alert_type, 1.0)
        return int(base_score * multiplier)

    def get_active_alerts(self, limit: int = 50) -> List[Dict]:
        """Get active alerts sorted by priority and time"""
        active = [alert for alert in self.active_alerts if not alert['resolved']]
        # Sort by priority score (desc) then timestamp (desc)
        active.sort(key=lambda x: (x['priority_score'], x['timestamp']), reverse=True)
        return active[:limit]

    def create_emergency_alert(self):
        """Create emergency protocol alert"""
        return self.create_alert(
            "emergency",
            "critical",
            "🚨 Emergency Protocol Activated",
            "Emergency protocol has been manually activated. All active drones are being recalled to base station immediately.",
            "Manual Override",
            {"emergency_type": "manual_activation", "all_drones_affected": True}
        )

    def simulate_real_time_alerts(self):
        """Generate realistic alerts based on operational scenarios"""
        # Battery alerts
        if random.random() < 0.08:  # 8% chance
            drone_id = f"LLA-{random.randint(1, 15):03d}"
            battery_level = random.randint(5, 20)
            severity = "critical" if battery_level <= 15 else "warning"

            self.create_alert(
                "drone_battery",
                severity,
                f"{'Critical' if severity == 'critical' else 'Low'} Battery Alert",
                f"Drone {drone_id} battery level at {battery_level}%. {'Immediate landing required' if severity == 'critical' else 'Consider returning to base'}.",
                drone_id,
                {"drone_id": drone_id, "battery_level": battery_level}
            )

        # Medical supply alerts
        if random.random() < 0.05:  # 5% chance
            supplies = ["Blood Pack O+", "Emergency Medications", "IV Fluids", "Trauma Kit"]
            item = random.choice(supplies)
            stock_level = random.randint(1, 8)

            self.create_alert(
                "medical_supply",
                "warning",
                f"Low Stock Alert - {item}",
                f"{item} stock is running low. Current level: {stock_level} units remaining.",
                "Inventory System",
                {"item_name": item, "stock_level": stock_level}
            )

        # Weather alerts
        if random.random() < 0.03:  # 3% chance
            weather_conditions = ["High winds (25+ km/h)", "Heavy precipitation", "Low visibility", "Thunderstorm approaching"]
            condition = random.choice(weather_conditions)

            self.create_alert(
                "weather",
                "warning",
                "Weather Advisory",
                f"Adverse weather detected: {condition}. Flight operations may be impacted.",
                "Weather Service",
                {"condition": condition, "advisory_level": "caution"}
            )

        # System health alerts
        if random.random() < 0.02:  # 2% chance
            system_issues = [
                ("Communication", "Intermittent GPS signal loss detected"),
                ("Temperature", "Cold storage unit temperature fluctuation"),
                ("Network", "Reduced network connectivity in Zone Beta")
            ]
            system, issue = random.choice(system_issues)

            self.create_alert(
                "system_health",
                "info",
                f"{system} Status Update",
                issue,
                "System Monitor",
                {"system_component": system}
            )

    def _log_activity(self, description: str, activity_type: str):
        """Log system activities for audit trail"""
        activity = {
            'timestamp': datetime.now(),
            'type': activity_type,
            'description': description,
            'user': 'System'
        }

        self.recent_activities.append(activity)

        # Keep last 100 activities
        if len(self.recent_activities) > 100:
            self.recent_activities = self.recent_activities[-100:]

    def get_recent_activities(self, limit: int = 20) -> List[Dict]:
        """Get recent system activities"""
        # Generate initial activities if empty
        if not self.recent_activities:
            initial_activities = [
                ("System initialization completed successfully", "system"),
                ("Weather data synchronization active", "system"),
                ("Drone fleet status monitoring enabled", "system"),
                ("Medical inventory tracking online", "system"),
                ("Emergency protocols loaded and verified", "system"),
                ("Communication systems operational", "system"),
                ("GPS tracking calibration complete", "system"),
                ("Temperature monitoring systems active", "system")
            ]

            for i, (desc, activity_type) in enumerate(initial_activities):
                self.recent_activities.append({
                    'timestamp': datetime.now() - timedelta(minutes=i*5),
                    'type': activity_type,
                    'description': desc,
                    'user': 'System'
                })

        return sorted(self.recent_activities, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def get_alert_statistics(self) -> Dict:
        """Get comprehensive alert statistics"""
        active = self.get_active_alerts()

        # Severity breakdown
        severity_counts = {'critical': 0, 'warning': 0, 'info': 0, 'success': 0}
        for alert in active:
            severity_counts[alert['severity']] += 1

        # Type breakdown
        type_counts = {}
        for alert in active:
            alert_type = alert['type']
            type_counts[alert_type] = type_counts.get(alert_type, 0) + 1

        # Time-based analysis
        recent_alerts = [a for a in active if (datetime.now() - a['timestamp']).total_seconds() < 3600]  # Last hour

        return {
            'total_active': len(active),
            'total_resolved_today': len([a for a in self.alert_history 
                                       if a.get('resolved_at', datetime.min).date() == datetime.now().date()]),
            'severity_breakdown': severity_counts,
            'type_breakdown': type_counts,
            'recent_alerts_1h': len(recent_alerts),
            'average_resolution_time': self._calculate_avg_resolution_time()
        }

    def _calculate_avg_resolution_time(self) -> float:
        """Calculate average alert resolution time in minutes"""
        resolved_today = [a for a in self.alert_history 
                         if a.get('resolved_at', datetime.min).date() == datetime.now().date()]

        if not resolved_today:
            return 0.0

        total_time = sum(
            (a['resolved_at'] - a['timestamp']).total_seconds() / 60 
            for a in resolved_today 
            if 'resolved_at' in a
        )

        return round(total_time / len(resolved_today), 1)

    def acknowledge_alert(self, alert_id: str, user: str = "System") -> bool:
        """Acknowledge an alert"""
        for alert in self.active_alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                alert['acknowledged_by'] = user
                alert['acknowledged_at'] = datetime.now()
                self._log_activity(f"Alert {alert_id} acknowledged by {user}", "alert_action")
                return True
        return False

    def resolve_alert(self, alert_id: str, user: str = "System", notes: str = "") -> bool:
        """Resolve an alert and move to history"""
        for i, alert in enumerate(self.active_alerts):
            if alert['id'] == alert_id:
                alert['resolved'] = True
                alert['resolved_by'] = user
                alert['resolved_at'] = datetime.now()
                alert['resolution_notes'] = notes

                # Move to history
                self.alert_history.append(alert)
                self.active_alerts.pop(i)

                self._log_activity(f"Alert {alert_id} resolved by {user}", "alert_action")
                return True
        return False

    def get_critical_alert_summary(self) -> Dict:
        """Get summary of critical alerts for dashboard"""
        critical_alerts = [a for a in self.get_active_alerts() if a['severity'] == 'critical']
        warning_alerts = [a for a in self.get_active_alerts() if a['severity'] == 'warning']

        return {
            'critical_count': len(critical_alerts),
            'warning_count': len(warning_alerts),
            'latest_critical': critical_alerts[0] if critical_alerts else None,
            'system_status': 'critical' if critical_alerts else ('warning' if warning_alerts else 'operational')
        }
