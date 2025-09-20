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

st.set_page_config(page_title="Fleet Dashboard", page_icon="🚁", layout="wide")

st.title("🚁 Fleet Dashboard")
st.markdown("Real-time monitoring of VTOL medical drone fleet")

# Simulated drone data
def get_fleet_data():
    drone_ids = [f"LLA-{i:03d}" for i in range(1, 16)]
    statuses = ['Active', 'Charging', 'Maintenance', 'Emergency']
    missions = ['Medical Delivery', 'Search & Rescue', 'Supply Drop', 'Reconnaissance', 'Standby']
    locations = ['Zone Alpha', 'Zone Beta', 'Zone Gamma', 'Base Station', 'En Route']

    data = []
    for drone_id in drone_ids:
        data.append({
            'id': drone_id,
            'status': np.random.choice(statuses, p=[0.6, 0.2, 0.15, 0.05]),
            'battery': np.random.randint(15, 100),
            'mission': np.random.choice(missions),
            'location': np.random.choice(locations),
            'lat': 28.6139 + np.random.uniform(-0.05, 0.05),
            'lon': 77.2090 + np.random.uniform(-0.05, 0.05),
            'last_update': datetime.now() - timedelta(minutes=np.random.randint(0, 30))
        })
    return data

# Get fleet data
fleet_data = get_fleet_data()
df = pd.DataFrame(fleet_data)

# Fleet metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_drones = len(df)
    st.metric("🚁 Total Drones", total_drones)

with col2:
    active_drones = len(df[df['status'] == 'Active'])
    st.metric("🟢 Active", active_drones, f"+{np.random.randint(0, 3)}")

with col3:
    charging_drones = len(df[df['status'] == 'Charging'])
    st.metric("🔋 Charging", charging_drones)

with col4:
    maintenance_drones = len(df[df['status'] == 'Maintenance'])
    st.metric("🔧 Maintenance", maintenance_drones)

with col5:
    avg_battery = df['battery'].mean()
    st.metric("⚡ Avg Battery", f"{avg_battery:.1f}%")

# Main dashboard
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎛️ Fleet Status")

    # Status distribution
    status_counts = df['status'].value_counts()
    fig_pie = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Fleet Status Distribution",
        color_discrete_map={
            'Active': '#4CAF50',
            'Charging': '#FF9800', 
            'Maintenance': '#F44336',
            'Emergency': '#9C27B0'
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Battery levels
    fig_battery = px.histogram(
        df, x='battery', 
        title='Battery Level Distribution',
        nbins=10,
        color_discrete_sequence=['#4ECDC4']
    )
    st.plotly_chart(fig_battery, use_container_width=True)

with col_right:
    st.subheader("🗺️ Fleet Location Map")

    # Create map
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=11)

    # Add drone markers
    for _, drone in df.iterrows():
        color_map = {
            'Active': 'green',
            'Charging': 'orange',
            'Maintenance': 'red', 
            'Emergency': 'purple'
        }

        folium.Marker(
            [drone['lat'], drone['lon']],
            popup=f"{drone['id']}: {drone['status']} ({drone['battery']}%)",
            tooltip=f"{drone['id']} - {drone['mission']}",
            icon=folium.Icon(
                color=color_map.get(drone['status'], 'blue'),
                icon='helicopter',
                prefix='fa'
            )
        ).add_to(m)

    # Add base station
    folium.Circle(
        location=[28.6139, 77.2090],
        radius=2000,
        popup='Base Station',
        color='blue',
        fill=True,
        fillColor='lightblue',
        fillOpacity=0.3
    ).add_to(m)

    map_data = st_folium(m, width=700, height=400)

# Detailed fleet table
st.subheader("📋 Detailed Fleet Information")

# Configure table columns
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
    "mission": "Mission",
    "location": "Location",
    "last_update": st.column_config.DatetimeColumn(
        "Last Update",
        format="HH:mm:ss"
    )
}

# Display table
st.dataframe(
    df[['id', 'status', 'battery', 'mission', 'location', 'last_update']],
    use_container_width=True,
    column_config=column_config,
    hide_index=True
)

# Quick actions
st.subheader("⚡ Quick Actions")

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    if st.button("🚨 Emergency Recall", use_container_width=True):
        st.success("Emergency recall signal sent to all active drones!")

with col_b:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

with col_c:
    if st.button("📊 Generate Report", use_container_width=True):
        st.info("Fleet status report generated!")

with col_d:
    if st.button("⚙️ Fleet Settings", use_container_width=True):
        st.info("Redirecting to fleet settings...")
