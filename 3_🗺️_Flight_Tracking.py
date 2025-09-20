import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Flight Tracking", page_icon="🗺️", layout="wide")

st.title("🗺️ Live Flight Tracking")
st.markdown("Real-time GPS tracking and route visualization for VTOL medical drones")

# Generate flight data
def generate_flight_data():
    # Base coordinates (Delhi area for example)
    base_lat, base_lon = 28.6139, 77.2090

    flights = []
    for i in range(5):
        # Generate flight path
        start_lat = base_lat + np.random.uniform(-0.02, 0.02)
        start_lon = base_lon + np.random.uniform(-0.02, 0.02)
        end_lat = base_lat + np.random.uniform(-0.05, 0.05)
        end_lon = base_lon + np.random.uniform(-0.05, 0.05)

        # Create path points
        num_points = 20
        path_lats = np.linspace(start_lat, end_lat, num_points)
        path_lons = np.linspace(start_lon, end_lon, num_points)

        # Add some realistic deviation
        path_lats += np.random.normal(0, 0.0005, num_points)
        path_lons += np.random.normal(0, 0.0005, num_points)

        flights.append({
            'drone_id': f'LLA-{i+1:03d}',
            'status': np.random.choice(['Active', 'Returning', 'Landed']),
            'current_lat': path_lats[-5],  # Current position
            'current_lon': path_lons[-5],
            'path_lats': path_lats.tolist(),
            'path_lons': path_lons.tolist(),
            'destination': f'Medical Station {chr(65+i)}',
            'altitude': np.random.uniform(50, 150),
            'speed': np.random.uniform(45, 85),
            'eta': datetime.now() + timedelta(minutes=np.random.randint(5, 30)),
            'battery': np.random.randint(40, 95),
            'mission_type': np.random.choice(['Emergency Delivery', 'Scheduled Supply', 'Search & Rescue'])
        })

    return flights

flight_data = generate_flight_data()

# Flight status overview
st.subheader("✈️ Active Flight Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    active_flights = len([f for f in flight_data if f['status'] == 'Active'])
    st.metric("🚁 Active Flights", active_flights)

with col2:
    avg_altitude = np.mean([f['altitude'] for f in flight_data])
    st.metric("📏 Avg Altitude", f"{avg_altitude:.0f}m")

with col3:
    avg_speed = np.mean([f['speed'] for f in flight_data])
    st.metric("💨 Avg Speed", f"{avg_speed:.0f} km/h")

with col4:
    total_distance = sum([np.random.uniform(10, 30) for _ in flight_data])
    st.metric("🛣️ Total Distance", f"{total_distance:.0f} km")

# Main map and flight details
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🗺️ Real-time Flight Map")

    # Create the main tracking map
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=12)

    # Add base station
    folium.Marker(
        [28.6139, 77.2090],
        popup="🏥 Base Station - Life-Line Air HQ",
        tooltip="Base Station",
        icon=folium.Icon(color='blue', icon='home', prefix='fa')
    ).add_to(m)

    # Colors for different flight statuses
    status_colors = {
        'Active': '#4CAF50',
        'Returning': '#FF9800', 
        'Landed': '#9E9E9E'
    }

    # Add flight paths and current positions
    for flight in flight_data:
        # Flight path
        path_coordinates = list(zip(flight['path_lats'], flight['path_lons']))

        folium.PolyLine(
            path_coordinates,
            color=status_colors.get(flight['status'], '#2196F3'),
            weight=3,
            opacity=0.7,
            popup=f"{flight['drone_id']} - {flight['mission_type']}"
        ).add_to(m)

        # Current drone position
        popup_html = f"""
        <div style="width: 200px;">
            <h4>{flight['drone_id']}</h4>
            <p><b>Status:</b> {flight['status']}</p>
            <p><b>Mission:</b> {flight['mission_type']}</p>
            <p><b>Destination:</b> {flight['destination']}</p>
            <p><b>Altitude:</b> {flight['altitude']:.0f}m</p>
            <p><b>Speed:</b> {flight['speed']:.0f} km/h</p>
            <p><b>Battery:</b> {flight['battery']}%</p>
            <p><b>ETA:</b> {flight['eta'].strftime('%H:%M')}</p>
        </div>
        """

        folium.Marker(
            [flight['current_lat'], flight['current_lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{flight['drone_id']} - {flight['status']}",
            icon=folium.Icon(
                color='green' if flight['status'] == 'Active' else 'orange',
                icon='helicopter',
                prefix='fa'
            )
        ).add_to(m)

        # Add destination marker
        dest_lat = flight['path_lats'][-1]
        dest_lon = flight['path_lons'][-1]

        folium.CircleMarker(
            [dest_lat, dest_lon],
            radius=8,
            popup=f"Destination: {flight['destination']}",
            color=status_colors.get(flight['status'], '#2196F3'),
            fill=True,
            weight=2
        ).add_to(m)

    # Add no-fly zones (example)
    folium.Circle(
        [28.6239, 77.2190],
        radius=1000,
        popup='Restricted Airspace',
        color='red',
        fill=True,
        fillColor='red',
        fillOpacity=0.2,
        weight=2
    ).add_to(m)

    # Display map
    map_data = st_folium(m, width=800, height=500)

with col_right:
    st.subheader("📋 Flight Details")

    # Flight information cards
    for flight in flight_data:
        status_color = {
            'Active': '#4CAF50',
            'Returning': '#FF9800',
            'Landed': '#9E9E9E'
        }.get(flight['status'], '#2196F3')

        st.markdown(f"""
        <div style="border: 2px solid {status_color}; border-radius: 10px; padding: 15px; margin: 10px 0; background: white;">
            <h4 style="margin: 0; color: {status_color};">{flight['drone_id']}</h4>
            <p style="margin: 5px 0;"><b>Status:</b> {flight['status']}</p>
            <p style="margin: 5px 0;"><b>Mission:</b> {flight['mission_type']}</p>
            <p style="margin: 5px 0;"><b>Destination:</b> {flight['destination']}</p>
            <p style="margin: 5px 0;"><b>Altitude:</b> {flight['altitude']:.0f}m</p>
            <p style="margin: 5px 0;"><b>Speed:</b> {flight['speed']:.0f} km/h</p>
            <p style="margin: 5px 0;"><b>Battery:</b> {flight['battery']}%</p>
            <p style="margin: 5px 0;"><b>ETA:</b> {flight['eta'].strftime('%H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick actions for each flight
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"📞 Contact", key=f"contact_{flight['drone_id']}"):
                st.success(f"Contacting {flight['drone_id']}")
        with col_b:
            if st.button(f"🏠 Return", key=f"return_{flight['drone_id']}"):
                st.info(f"{flight['drone_id']} returning to base")

# Flight analytics
st.subheader("📊 Flight Analytics")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Altitude vs Speed scatter plot
    altitudes = [f['altitude'] for f in flight_data]
    speeds = [f['speed'] for f in flight_data]
    drone_ids = [f['drone_id'] for f in flight_data]

    fig_scatter = px.scatter(
        x=altitudes,
        y=speeds,
        text=drone_ids,
        title="Altitude vs Speed Analysis",
        labels={'x': 'Altitude (m)', 'y': 'Speed (km/h)'},
        color=speeds,
        color_continuous_scale='Viridis'
    )
    fig_scatter.update_traces(textposition="top center")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_chart2:
    # Battery levels
    batteries = [f['battery'] for f in flight_data]
    drone_labels = [f['drone_id'] for f in flight_data]

    fig_battery = px.bar(
        x=drone_labels,
        y=batteries,
        title="Current Battery Levels",
        labels={'x': 'Drone ID', 'y': 'Battery (%)'},
        color=batteries,
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_battery, use_container_width=True)

# Weather information
st.subheader("🌤️ Weather Conditions")

col_w1, col_w2, col_w3, col_w4 = st.columns(4)

with col_w1:
    st.metric("🌡️ Temperature", "24°C", "-2°C")

with col_w2:
    st.metric("💨 Wind Speed", "15 km/h", "+3 km/h")

with col_w3:
    st.metric("👁️ Visibility", "10 km", "No change")

with col_w4:
    st.metric("☁️ Cloud Cover", "30%", "-10%")

# Weather alerts
weather_alerts = [
    "🟢 Flight conditions optimal for all operations",
    "🟡 Moderate crosswinds in Zone Alpha - exercise caution", 
    "🟢 No precipitation expected in next 4 hours"
]

st.subheader("⚠️ Weather Alerts")
for alert in weather_alerts:
    if "🟢" in alert:
        st.success(alert)
    elif "🟡" in alert:
        st.warning(alert)
    elif "🔴" in alert:
        st.error(alert)

# Control panel
st.subheader("🎛️ Flight Control")

col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)

with col_ctrl1:
    if st.button("🚨 Emergency Landing", use_container_width=True):
        st.error("Emergency landing protocol activated for all flights!")

with col_ctrl2:
    if st.button("🏠 Return All", use_container_width=True):
        st.info("Return-to-base command sent to all active drones")

with col_ctrl3:
    if st.button("📡 Refresh Tracking", use_container_width=True):
        st.success("GPS tracking data refreshed")

with col_ctrl4:
    if st.button("📋 Flight Log", use_container_width=True):
        st.info("Opening detailed flight log...")

# Auto-refresh toggle
with st.sidebar:
    st.subheader("🔄 Auto Refresh")
    auto_refresh = st.toggle("Enable Auto Refresh")
    refresh_interval = st.select_slider(
        "Refresh Interval", 
        options=[5, 10, 15, 30],
        value=10,
        format_func=lambda x: f"{x} seconds"
    )

    if auto_refresh:
        st.info(f"Auto-refreshing every {refresh_interval} seconds")
        # In a real app, you would implement auto-refresh here

    st.subheader("🎯 Quick Filters")
    show_active = st.checkbox("Show Active Flights", value=True)
    show_returning = st.checkbox("Show Returning Flights", value=True)
    show_paths = st.checkbox("Show Flight Paths", value=True)
    show_weather = st.checkbox("Show Weather Overlay", value=False)
