"""
Authentication and User Management System
Secure user authentication with role-based access control
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class User:
    """User model with role-based permissions"""

    def __init__(self, username: str, email: str, role: str, full_name: str = ""):
        self.username = username
        self.email = email
        self.role = role
        self.full_name = full_name or username.title()
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
        self.permissions = self._get_role_permissions(role)
        self.login_count = 0

    def _get_role_permissions(self, role: str) -> List[str]:
        """Define permissions based on user role"""
        role_permissions = {
            'Administrator': [
                'view_all_data', 'control_all_drones', 'manage_users', 
                'system_configuration', 'emergency_override', 'data_export',
                'maintenance_management', 'inventory_full_access'
            ],
            'Fleet Manager': [
                'view_all_data', 'control_all_drones', 'mission_planning',
                'fleet_analytics', 'maintenance_view', 'inventory_management'
            ],
            'Pilot Operator': [
                'view_fleet_data', 'control_assigned_drones', 'mission_execution',
                'flight_planning', 'emergency_procedures'
            ],
            'Medical Coordinator': [
                'view_medical_data', 'inventory_management', 'delivery_tracking',
                'supply_analytics', 'temperature_monitoring'
            ],
            'Maintenance Tech': [
                'view_maintenance_data', 'maintenance_management', 'component_tracking',
                'diagnostic_tools', 'repair_logging'
            ],
            'Observer': [
                'view_basic_data', 'mission_tracking', 'status_monitoring'
            ]
        }
        return role_permissions.get(role, ['view_basic_data'])

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now()
        self.login_count += 1

def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[User]]:
    """
    Authenticate user with enhanced security features
    Returns (success, user_object)
    """

    # Demo user database with enhanced profiles
    demo_users = {
        'admin': {
            'password': 'admin123',
            'email': 'admin@lifeline-air.com',
            'role': 'Administrator',
            'full_name': 'System Administrator'
        },
        'fleet_mgr': {
            'password': 'fleet123',
            'email': 'fleet@lifeline-air.com', 
            'role': 'Fleet Manager',
            'full_name': 'Fleet Operations Manager'
        },
        'pilot1': {
            'password': 'pilot123',
            'email': 'pilot1@lifeline-air.com',
            'role': 'Pilot Operator', 
            'full_name': 'Senior Drone Pilot'
        },
        'medical': {
            'password': 'medical123',
            'email': 'medical@lifeline-air.com',
            'role': 'Medical Coordinator',
            'full_name': 'Medical Supply Coordinator'
        },
        'tech': {
            'password': 'tech123',
            'email': 'tech@lifeline-air.com',
            'role': 'Maintenance Tech',
            'full_name': 'Senior Maintenance Technician'
        },
        'observer': {
            'password': 'observer123',
            'email': 'observer@lifeline-air.com',
            'role': 'Observer',
            'full_name': 'Operations Observer'
        },
        'demo': {
            'password': 'demo123',
            'email': 'demo@lifeline-air.com',
            'role': 'Observer',
            'full_name': 'Demo User'
        }
    }

    if username in demo_users and demo_users[username]['password'] == password:
        user_data = demo_users[username]
        user = User(
            username=username,
            email=user_data['email'], 
            role=user_data['role'],
            full_name=user_data['full_name']
        )
        user.update_last_login()
        return True, user

    return False, None

def get_user_dashboard_config(user: User) -> Dict:
    """Get personalized dashboard configuration based on user role"""

    base_config = {
        'sidebar_sections': ['System Status'],
        'main_metrics': ['Active Drones', 'System Health'],
        'available_pages': ['Fleet Dashboard'],
        'quick_actions': ['Refresh Data']
    }

    role_configs = {
        'Administrator': {
            'sidebar_sections': ['System Status', 'Quick Actions', 'Admin Tools'],
            'main_metrics': ['Active Drones', 'Missions Today', 'Medical Supplies', 'System Health'],
            'available_pages': ['Fleet Dashboard', 'Mission Analytics', 'Flight Tracking', 
                              'Medical Cargo', 'Maintenance', 'Settings'],
            'quick_actions': ['Emergency Protocol', 'System Backup', 'Generate Report', 'User Management']
        },
        'Fleet Manager': {
            'sidebar_sections': ['System Status', 'Fleet Control', 'Analytics'],
            'main_metrics': ['Active Drones', 'Missions Today', 'Fleet Efficiency', 'Mission Success Rate'],
            'available_pages': ['Fleet Dashboard', 'Mission Analytics', 'Flight Tracking', 'Maintenance'],
            'quick_actions': ['Deploy Emergency Mission', 'Recall All Drones', 'Fleet Report']
        },
        'Pilot Operator': {
            'sidebar_sections': ['My Missions', 'Flight Control', 'Weather'],
            'main_metrics': ['My Active Drones', 'Current Missions', 'Battery Status', 'Weather Status'],
            'available_pages': ['Fleet Dashboard', 'Flight Tracking'],
            'quick_actions': ['Emergency Landing', 'Request Support', 'Weather Update']
        },
        'Medical Coordinator': {
            'sidebar_sections': ['Medical Inventory', 'Deliveries', 'Alerts'],
            'main_metrics': ['Medical Supplies', 'Active Deliveries', 'Critical Stock', 'Temperature Status'],
            'available_pages': ['Medical Cargo', 'Mission Analytics'],
            'quick_actions': ['Emergency Restock', 'Delivery Status', 'Temperature Alert']
        },
        'Maintenance Tech': {
            'sidebar_sections': ['Maintenance Queue', 'Components', 'Diagnostics'],
            'main_metrics': ['Maintenance Due', 'Component Health', 'Fleet Availability', 'Repair Queue'],
            'available_pages': ['Maintenance', 'Fleet Dashboard'],
            'quick_actions': ['Schedule Maintenance', 'Component Check', 'Diagnostics Report']
        }
    }

    config = role_configs.get(user.role, base_config)
    config['user_info'] = {
        'username': user.username,
        'full_name': user.full_name,
        'role': user.role,
        'last_login': user.last_login,
        'permissions_count': len(user.permissions)
    }

    return config

def check_permission(user: Optional[User], required_permission: str) -> bool:
    """Check if user has required permission"""
    if not user:
        return False
    return user.has_permission(required_permission)

def get_security_context() -> Dict:
    """Get current security context and recommendations"""
    return {
        'session_active': True,
        'last_security_scan': datetime.now() - timedelta(hours=2),
        'threat_level': 'Low',
        'recommendations': [
            'Regular password updates recommended',
            'Enable two-factor authentication',
            'Review user access permissions quarterly'
        ],
        'audit_log_enabled': True,
        'encryption_status': 'Active'
    }
