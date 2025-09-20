import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ System Settings & Configuration")
st.markdown("Configure system parameters, user management, and application preferences")

# Initialize session state for settings
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'notifications': {
            'email_alerts': True,
            'sms_alerts': False,
            'push_notifications': True,
            'alert_threshold_battery': 20,
            'alert_threshold_stock': 10
        },
        'system': {
            'auto_refresh_interval': 30,
            'map_default_zoom': 12,
            'temperature_unit': 'Celsius',
            'distance_unit': 'Kilometers',
            'max_flight_altitude': 150,
            'emergency_landing_battery': 15
        },
        'display': {
            'theme': 'Light',
            'chart_color_scheme': 'Default',
            'dashboard_layout': 'Standard',
            'show_animations': True,
            'compact_view': False
        },
        'security': {
            'session_timeout': 30,
            'require_2fa': False,
            'audit_logging': True,
            'data_encryption': True,
            'api_rate_limiting': True
        }
    }

# Settings navigation
st.subheader("🎛️ Settings Categories")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔔 Notifications", 
    "⚙️ System", 
    "🎨 Display", 
    "🔒 Security", 
    "👥 Users", 
    "🔧 Advanced"
])

with tab1:
    st.header("🔔 Notification Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Alert Preferences")

        email_alerts = st.checkbox(
            "Email Alerts", 
            value=st.session_state.settings['notifications']['email_alerts']
        )

        sms_alerts = st.checkbox(
            "SMS Alerts", 
            value=st.session_state.settings['notifications']['sms_alerts']
        )

        push_notifications = st.checkbox(
            "Push Notifications", 
            value=st.session_state.settings['notifications']['push_notifications']
        )

        # Alert thresholds
        st.subheader("Alert Thresholds")

        battery_threshold = st.slider(
            "Low Battery Alert (%)",
            min_value=5,
            max_value=50,
            value=st.session_state.settings['notifications']['alert_threshold_battery'],
            step=5
        )

        stock_threshold = st.slider(
            "Low Stock Alert (units)",
            min_value=1,
            max_value=50,
            value=st.session_state.settings['notifications']['alert_threshold_stock'],
            step=1
        )

    with col2:
        st.subheader("Notification Schedule")

        # Notification time settings
        quiet_hours_start = st.time_input("Quiet Hours Start", value=datetime.strptime("22:00", "%H:%M").time())
        quiet_hours_end = st.time_input("Quiet Hours End", value=datetime.strptime("06:00", "%H:%M").time())

        emergency_override = st.checkbox("Override Quiet Hours for Emergencies", value=True)

        st.subheader("Alert Recipients")

        # Email recipients
        with st.form("email_recipients"):
            st.write("**Email Recipients**")
            recipient_email = st.text_input("Email Address")
            recipient_role = st.selectbox("Role", ["Administrator", "Operator", "Technician", "Observer"])

            if st.form_submit_button("Add Recipient"):
                if recipient_email:
                    st.success(f"Added {recipient_email} as {recipient_role}")

        # Display current recipients (mock data)
        st.write("**Current Recipients:**")
        recipients = [
            {"email": "admin@lifeline-air.com", "role": "Administrator", "active": True},
            {"email": "ops@lifeline-air.com", "role": "Operator", "active": True},
            {"email": "tech@lifeline-air.com", "role": "Technician", "active": False}
        ]

        for recipient in recipients:
            status = "🟢" if recipient['active'] else "🔴"
            st.write(f"{status} {recipient['email']} - {recipient['role']}")

with tab2:
    st.header("⚙️ System Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Application Settings")

        auto_refresh = st.selectbox(
            "Auto Refresh Interval",
            options=[5, 10, 15, 30, 60],
            index=3,  # 30 seconds default
            format_func=lambda x: f"{x} seconds"
        )

        map_zoom = st.slider(
            "Default Map Zoom Level",
            min_value=8,
            max_value=18,
            value=st.session_state.settings['system']['map_default_zoom'],
            step=1
        )

        temp_unit = st.radio(
            "Temperature Unit",
            options=["Celsius", "Fahrenheit"],
            index=0
        )

        distance_unit = st.radio(
            "Distance Unit", 
            options=["Kilometers", "Miles"],
            index=0
        )

    with col2:
        st.subheader("Operational Parameters")

        max_altitude = st.number_input(
            "Maximum Flight Altitude (meters)",
            min_value=50,
            max_value=500,
            value=st.session_state.settings['system']['max_flight_altitude'],
            step=10
        )

        emergency_battery = st.number_input(
            "Emergency Landing Battery Level (%)",
            min_value=5,
            max_value=30,
            value=st.session_state.settings['system']['emergency_landing_battery'],
            step=1
        )

        max_payload = st.number_input(
            "Maximum Payload Weight (kg)",
            min_value=1.0,
            max_value=10.0,
            value=5.0,
            step=0.1
        )

        flight_time_limit = st.number_input(
            "Maximum Flight Time (minutes)",
            min_value=30,
            max_value=180,
            value=120,
            step=5
        )

with tab3:
    st.header("🎨 Display & Interface")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Appearance")

        theme = st.radio(
            "Application Theme",
            options=["Light", "Dark", "Auto"],
            index=0
        )

        color_scheme = st.selectbox(
            "Chart Color Scheme",
            options=["Default", "Viridis", "Plasma", "Inferno", "Turbo"],
            index=0
        )

        layout = st.radio(
            "Dashboard Layout",
            options=["Standard", "Compact", "Wide"],
            index=0
        )

        animations = st.checkbox("Enable Animations", value=True)
        compact_view = st.checkbox("Compact Card View", value=False)

    with col2:
        st.subheader("Data Display")

        decimal_places = st.number_input(
            "Decimal Places for Metrics",
            min_value=0,
            max_value=4,
            value=1,
            step=1
        )

        date_format = st.selectbox(
            "Date Format",
            options=["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
            index=0
        )

        time_format = st.radio(
            "Time Format",
            options=["24 Hour", "12 Hour AM/PM"],
            index=0
        )

        # Preview
        st.subheader("Preview")
        sample_date = datetime.now()

        if date_format == "DD/MM/YYYY":
            date_preview = sample_date.strftime("%d/%m/%Y")
        elif date_format == "MM/DD/YYYY":
            date_preview = sample_date.strftime("%m/%d/%Y")
        else:
            date_preview = sample_date.strftime("%Y-%m-%d")

        if time_format == "24 Hour":
            time_preview = sample_date.strftime("%H:%M:%S")
        else:
            time_preview = sample_date.strftime("%I:%M:%S %p")

        st.info(f"Date: {date_preview} | Time: {time_preview}")

with tab4:
    st.header("🔒 Security Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Authentication")

        session_timeout = st.number_input(
            "Session Timeout (minutes)",
            min_value=5,
            max_value=120,
            value=st.session_state.settings['security']['session_timeout'],
            step=5
        )

        require_2fa = st.checkbox(
            "Require Two-Factor Authentication",
            value=st.session_state.settings['security']['require_2fa']
        )

        password_complexity = st.checkbox("Enforce Strong Passwords", value=True)

        login_attempts = st.number_input(
            "Max Login Attempts",
            min_value=3,
            max_value=10,
            value=5,
            step=1
        )

    with col2:
        st.subheader("Data Protection")

        audit_logging = st.checkbox(
            "Enable Audit Logging",
            value=st.session_state.settings['security']['audit_logging']
        )

        data_encryption = st.checkbox(
            "Enable Data Encryption",
            value=st.session_state.settings['security']['data_encryption']
        )

        api_rate_limiting = st.checkbox(
            "API Rate Limiting",
            value=st.session_state.settings['security']['api_rate_limiting']
        )

        backup_frequency = st.selectbox(
            "Backup Frequency",
            options=["Daily", "Weekly", "Monthly"],
            index=0
        )

        # Security status
        st.subheader("Security Status")

        security_checks = [
            {"check": "SSL Certificate", "status": "Valid", "color": "green"},
            {"check": "Database Encryption", "status": "Active", "color": "green"},
            {"check": "Firewall", "status": "Active", "color": "green"},
            {"check": "Intrusion Detection", "status": "Active", "color": "green"},
            {"check": "Vulnerability Scan", "status": "Last: 2 days ago", "color": "orange"}
        ]

        for check in security_checks:
            status_icon = "🟢" if check["color"] == "green" else "🟡" if check["color"] == "orange" else "🔴"
            st.write(f"{status_icon} {check['check']}: {check['status']}")

with tab5:
    st.header("👥 User Management")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add New User")

        with st.form("add_user"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email Address")
            new_role = st.selectbox("Role", ["Administrator", "Operator", "Technician", "Observer"])
            new_department = st.selectbox("Department", ["Operations", "Maintenance", "Medical", "IT"])

            # Permissions
            st.write("**Permissions:**")
            view_fleet = st.checkbox("View Fleet Data", value=True)
            control_drones = st.checkbox("Control Drones")
            manage_inventory = st.checkbox("Manage Medical Inventory")
            system_admin = st.checkbox("System Administration")

            if st.form_submit_button("Create User"):
                if new_username and new_email:
                    st.success(f"User {new_username} created successfully!")

    with col2:
        st.subheader("Current Users")

        # Mock user data
        users_data = [
            {"username": "admin", "email": "admin@lifeline-air.com", "role": "Administrator", "status": "Active", "last_login": "2024-01-15 14:30"},
            {"username": "operator1", "email": "ops1@lifeline-air.com", "role": "Operator", "status": "Active", "last_login": "2024-01-15 09:15"},
            {"username": "tech1", "email": "tech1@lifeline-air.com", "role": "Technician", "status": "Active", "last_login": "2024-01-14 16:45"},
            {"username": "observer1", "email": "obs1@lifeline-air.com", "role": "Observer", "status": "Inactive", "last_login": "2024-01-10 11:20"}
        ]

        users_df = pd.DataFrame(users_data)

        st.dataframe(
            users_df,
            use_container_width=True,
            column_config={
                "username": "Username",
                "email": "Email",
                "role": "Role",
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Active", "Inactive", "Suspended"]
                ),
                "last_login": "Last Login"
            },
            hide_index=True
        )

        st.subheader("User Activity")

        # Recent activity log
        activities = [
            "admin logged in from 192.168.1.100",
            "operator1 deployed drone LLA-003",
            "tech1 completed maintenance on LLA-007", 
            "operator1 logged out",
            "admin changed system settings"
        ]

        for activity in activities[-5:]:
            st.write(f"• {activity}")

with tab6:
    st.header("🔧 Advanced Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("API Configuration")

        api_endpoint = st.text_input("API Endpoint", value="https://api.lifeline-air.com/v1")
        api_timeout = st.number_input("API Timeout (seconds)", min_value=5, max_value=60, value=30)
        max_requests = st.number_input("Max Requests per Minute", min_value=10, max_value=1000, value=100)

        st.subheader("Database Settings")

        db_host = st.text_input("Database Host", value="localhost")
        db_port = st.number_input("Database Port", min_value=1000, max_value=65535, value=5432)
        connection_pool = st.number_input("Connection Pool Size", min_value=5, max_value=50, value=20)

        st.subheader("Logging Configuration")

        log_level = st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        log_retention = st.number_input("Log Retention (days)", min_value=7, max_value=365, value=30)

    with col2:
        st.subheader("Performance Settings")

        cache_size = st.number_input("Cache Size (MB)", min_value=100, max_value=2000, value=512)
        max_concurrent = st.number_input("Max Concurrent Users", min_value=10, max_value=1000, value=100)

        st.subheader("Integration Settings")

        weather_api_key = st.text_input("Weather API Key", type="password")
        maps_api_key = st.text_input("Maps API Key", type="password")

        enable_weather = st.checkbox("Enable Weather Integration", value=True)
        enable_maps = st.checkbox("Enable Maps Integration", value=True)

        st.subheader("Maintenance Mode")

        maintenance_mode = st.checkbox("Enable Maintenance Mode", value=False)

        if maintenance_mode:
            st.warning("⚠️ Maintenance mode will restrict access to authorized users only")

            maintenance_message = st.text_area(
                "Maintenance Message",
                value="System is currently under maintenance. Please try again later."
            )

# Save Settings
st.subheader("💾 Save Configuration")

col_save1, col_save2, col_save3 = st.columns(3)

with col_save1:
    if st.button("💾 Save All Settings", use_container_width=True):
        # Update session state with current values
        st.session_state.settings['notifications']['email_alerts'] = email_alerts
        st.session_state.settings['notifications']['sms_alerts'] = sms_alerts
        st.session_state.settings['notifications']['push_notifications'] = push_notifications
        st.session_state.settings['notifications']['alert_threshold_battery'] = battery_threshold
        st.session_state.settings['notifications']['alert_threshold_stock'] = stock_threshold

        st.success("✅ All settings saved successfully!")

with col_save2:
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        st.warning("⚠️ This will reset all settings to default values")
        if st.button("Confirm Reset"):
            # Reset session state to defaults
            st.rerun()

with col_save3:
    if st.button("📤 Export Config", use_container_width=True):
        config_json = json.dumps(st.session_state.settings, indent=2, default=str)
        st.download_button(
            label="Download Configuration",
            data=config_json,
            file_name="lifeline_air_config.json",
            mime="application/json"
        )

# Configuration Status
st.subheader("📊 Configuration Status")

col_status1, col_status2, col_status3, col_status4 = st.columns(4)

with col_status1:
    st.metric("Active Users", "4", "+1")

with col_status2:
    st.metric("API Status", "Online", "")

with col_status3:
    st.metric("Database", "Connected", "")

with col_status4:
    last_backup = datetime.now() - timedelta(hours=6)
    st.metric("Last Backup", last_backup.strftime("%H:%M"), "6h ago")
