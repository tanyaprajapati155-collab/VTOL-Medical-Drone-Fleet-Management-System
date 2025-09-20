import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
from utils.drone_data import DroneDataManager
from utils.medical_supplies import MedicalSupplyManager
from utils.alerts import AlertManager
from utils.authentication import authenticate_user
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Life-Line Air VTOL Medical Drone System",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/lifeline-air',
        'Report a bug': "https://github.com/your-repo/lifeline-air/issues",
        'About': "Life-Line Air VTOL Medical Drone Delivery System v1.0"
    }
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #45B7D1);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-left: 5px solid #4ECDC4;
        margin: 1rem 0;
        transition: transform 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .alert-critical {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }

    .alert-warning {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border: 2px solid #ff9800;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }

    .alert-info {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    .drone-status-active {
        color: #4CAF50;
        font-weight: bold;
    }

    .drone-status-charging {
        color: #FF9800;
        font-weight: bold;
    }

    .drone-status-maintenance {
        color: #F44336;
        font-weight: bold;
    }

    .mission-success {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'drone_manager' not in st.session_state:
    st.session_state.drone_manager = DroneDataManager()
if 'medical_manager' not in st.session_state:
    st.session_state.medical_manager = MedicalSupplyManager()
if 'alert_manager' not in st.session_state:
    st.session_state.alert_manager = AlertManager()

def main():
    # Authentication check
    if not st.session_state.authenticated:
        show_login()
        return

    # Main application header
    st.markdown("""
    <div class="main-header">
        <h1>🚁 Life-Line Air VTOL Medical Drone System</h1>
        <h3>Autonomous Battlefield Medical Delivery Platform</h3>
        <p>Real-time Command & Control Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2 style="color: white; margin: 0;">🚁 Life-Line Air</h2>
            <p style="color: #E8EAF6; margin: 0; font-size: 0.9rem;">Mission Control</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Operator:** {st.session_state.username}")
        st.markdown(f"**Status:** Online 🟢")
        st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")

        st.markdown("---")

        # Quick Actions
        st.markdown("### 🎛️ Quick Actions")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚨 Emergency", use_container_width=True):
                st.session_state.alert_manager.create_emergency_alert()
                st.success("Emergency protocol activated!")

        with col2:
            if st.button("📊 Report", use_container_width=True):
                generate_mission_report()
                st.info("Generating report...")

        # Auto-refresh toggle
        st.markdown("---")
        auto_refresh = st.toggle("🔄 Auto Refresh", value=True)

        if auto_refresh:
            st.markdown("*Refreshing every 5 seconds*")

        # System status
        st.markdown("### 🔧 System Status")
        system_health = get_system_health()

        for component, status in system_health.items():
            status_color = "🟢" if status == "OK" else "🔴"
            st.markdown(f"{status_color} {component}: {status}")

        # Logout button
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Main dashboard content
    display_main_dashboard()

    # Auto-refresh mechanism
    if auto_refresh:
        time.sleep(5)
        st.rerun()

def show_login():
    """Display login interface"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h1>🚁 Life-Line Air</h1>
            <h3>VTOL Medical Drone System</h3>
            <p style="color: #666;">Secure Access Required</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                login_button = st.form_submit_button("🚀 Access Dashboard", use_container_width=True)

            if login_button:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Authentication successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

def display_main_dashboard():
    """Display the main dashboard content"""

    # Critical alerts section
    display_critical_alerts()

    # Main metrics
    display_key_metrics()

    # Fleet status overview
    display_fleet_overview()

    # Mission analytics
    display_mission_analytics()

    # Recent activities
    display_recent_activities()

def display_critical_alerts():
    """Display critical system alerts"""
    st.markdown("### 🚨 Critical Alerts")

    alerts = st.session_state.alert_manager.get_active_alerts()

    if not alerts:
        st.success("✅ All systems operational - No critical alerts")
        return

    for alert in alerts:
        alert_class = f"alert-{alert['severity'].lower()}"
        icon = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}[alert['severity'].lower()]

        st.markdown(f"""
        <div class="{alert_class}">
            <strong>{icon} {alert['title']}</strong><br>
            {alert['message']}<br>
            <small>🕐 {alert['timestamp'].strftime('%H:%M:%S')} | 📍 {alert.get('location', 'System')}</small>
        </div>
        """, unsafe_allow_html=True)

def display_key_metrics():
    """Display key performance metrics"""
    col1, col2, col3, col4 = st.columns(4)

    # Get real-time data
    fleet_data = st.session_state.drone_manager.get_fleet_overview()
    medical_data = st.session_state.medical_manager.get_inventory_overview()
    mission_data = st.session_state.drone_manager.get_mission_stats()

    with col1:
        st.metric(
            label="🚁 Active Drones",
            value=fleet_data['active'],
            delta=f"{fleet_data['change']:+d} from yesterday",
            delta_color="normal"
        )

    with col2:
        st.metric(
            label="📦 Missions Today", 
            value=mission_data['completed_today'],
            delta=f"{mission_data['change_percent']:+.1f}%",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="⚕️ Medical Supplies",
            value=f"{medical_data['availability']:.1f}%",
            delta=f"{medical_data['change']:+.1f}%",
            delta_color="inverse" if medical_data['change'] < 0 else "normal"
        )

    with col4:
        st.metric(
            label="⏱️ Avg Delivery Time",
            value=f"{mission_data['avg_delivery_time']:.1f} min",
            delta=f"{mission_data['delivery_time_change']:+.1f} min",
            delta_color="inverse"
        )

def display_fleet_overview():
    """Display fleet status overview"""
    st.markdown("### 🚁 Fleet Status Overview")

    # Get fleet data
    fleet_status = st.session_state.drone_manager.get_detailed_fleet_status()

    # Create DataFrame for display
    df = pd.DataFrame(fleet_status)

    # Custom column configuration
    column_config = {
        "id": "Drone ID",
        "status": st.column_config.SelectboxColumn(
            "Status",
            options=["Active", "Charging", "Maintenance", "Emergency"]
        ),
        "battery": st.column_config.ProgressColumn(
            "Battery %",
            min_value=0,
            max_value=100,
            format="%d%%"
        ),
        "mission": "Current Mission",
        "location": "Location",
        "last_update": st.column_config.DatetimeColumn(
            "Last Update",
            format="HH:mm:ss"
        )
    }

    # Display the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        column_config=column_config,
        hide_index=True
    )

    # Fleet statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        active_count = len([d for d in fleet_status if d['status'] == 'Active'])
        st.metric("🟢 Active", active_count)

    with col2:
        charging_count = len([d for d in fleet_status if d['status'] == 'Charging'])
        st.metric("🟡 Charging", charging_count)

    with col3:
        maintenance_count = len([d for d in fleet_status if d['status'] == 'Maintenance'])
        st.metric("🔴 Maintenance", maintenance_count)

def display_mission_analytics():
    """Display mission performance analytics"""
    st.markdown("### 📊 Mission Performance Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Mission success rate gauge
        success_rate = st.session_state.drone_manager.get_success_rate()

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=success_rate,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Mission Success Rate (%)"},
            delta={'reference': 95, 'position': "top"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 80], 'color': "lightgray"},
                    {'range': [80, 90], 'color': "yellow"},
                    {'range': [90, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))

        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Delivery time trends
        delivery_data = st.session_state.drone_manager.get_delivery_trends()

        fig_line = px.line(
            delivery_data,
            x='date',
            y='avg_delivery_time',
            title='Average Delivery Time Trend (7 days)',
            labels={'avg_delivery_time': 'Delivery Time (minutes)', 'date': 'Date'}
        )

        fig_line.update_traces(line_color='#4ECDC4', line_width=3)
        fig_line.update_layout(height=300)
        st.plotly_chart(fig_line, use_container_width=True)

    # Mission distribution pie chart
    col3, col4 = st.columns(2)

    with col3:
        mission_types = st.session_state.drone_manager.get_mission_distribution()

        fig_pie = px.pie(
            values=list(mission_types.values()),
            names=list(mission_types.keys()),
            title="Mission Type Distribution"
        )

        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        # Battery status distribution
        battery_data = st.session_state.drone_manager.get_battery_distribution()

        fig_bar = px.bar(
            x=list(battery_data.keys()),
            y=list(battery_data.values()),
            title="Fleet Battery Status",
            labels={'x': 'Battery Level', 'y': 'Number of Drones'}
        )

        fig_bar.update_traces(marker_color='#FF6B6B')
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)

def display_recent_activities():
    """Display recent system activities"""
    st.markdown("### 📝 Recent Activities")

    activities = st.session_state.alert_manager.get_recent_activities()

    for activity in activities[-10:]:  # Show last 10 activities
        icon = {
            'mission_completed': '✅',
            'drone_deployed': '🚀',
            'maintenance': '🔧',
            'alert': '⚠️',
            'supply_delivered': '📦'
        }.get(activity['type'], '📝')

        time_str = activity['timestamp'].strftime('%H:%M')

        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.2rem 0; background: #f8f9fa; border-radius: 5px; border-left: 3px solid #4ECDC4;">
            {icon} <strong>{time_str}</strong> - {activity['description']}
        </div>
        """, unsafe_allow_html=True)

def get_system_health():
    """Get overall system health status"""
    return {
        "Drone Fleet": "OK",
        "GPS Tracking": "OK", 
        "Communication": "OK",
        "Medical Inventory": "OK",
        "Weather Service": "OK",
        "Database": "OK"
    }

def generate_mission_report():
    """Generate mission performance report"""
    # This would generate a downloadable report
    pass

if __name__ == "__main__":
    main()
