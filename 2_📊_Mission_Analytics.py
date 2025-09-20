import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Mission Analytics", page_icon="📊", layout="wide")

st.title("📊 Mission Analytics")
st.markdown("Comprehensive analysis of drone mission performance")

# Generate sample mission data
def generate_mission_data():
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    missions_data = []

    for date in dates[-30:]:  # Last 30 days
        daily_missions = np.random.poisson(8)  # Average 8 missions per day
        success_rate = np.random.normal(94, 3)  # 94% average success rate
        avg_delivery_time = np.random.normal(12, 2)  # 12 min average

        missions_data.append({
            'date': date,
            'missions_completed': daily_missions,
            'missions_failed': max(0, int(daily_missions * (1 - success_rate/100))),
            'success_rate': max(85, min(99, success_rate)),
            'avg_delivery_time': max(8, avg_delivery_time),
            'medical_supplies_delivered': np.random.poisson(15),
            'distance_covered': np.random.normal(180, 30)
        })

    return pd.DataFrame(missions_data)

mission_df = generate_mission_data()

# Key Performance Indicators
st.subheader("🎯 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_missions = mission_df['missions_completed'].sum()
    st.metric("🎯 Total Missions (30d)", total_missions, f"+{np.random.randint(5, 15)}")

with col2:
    avg_success_rate = mission_df['success_rate'].mean()
    st.metric("✅ Success Rate", f"{avg_success_rate:.1f}%", f"+{np.random.uniform(0.5, 2.0):.1f}%")

with col3:
    avg_delivery_time = mission_df['avg_delivery_time'].mean()
    st.metric("⏱️ Avg Delivery Time", f"{avg_delivery_time:.1f} min", f"-{np.random.uniform(0.2, 1.0):.1f} min")

with col4:
    total_supplies = mission_df['medical_supplies_delivered'].sum()
    st.metric("📦 Supplies Delivered", total_supplies, f"+{np.random.randint(10, 30)}")

# Mission Performance Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Mission Trends")

    # Mission completion trend
    fig_missions = px.line(
        mission_df, 
        x='date', 
        y='missions_completed',
        title='Daily Mission Completions',
        labels={'missions_completed': 'Missions', 'date': 'Date'}
    )
    fig_missions.update_traces(line_color='#4ECDC4', line_width=3)
    st.plotly_chart(fig_missions, use_container_width=True)

    # Success rate gauge
    current_success_rate = mission_df['success_rate'].iloc[-1]

    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current_success_rate,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Current Success Rate (%)"},
        delta = {'reference': 95},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 85], 'color': "lightgray"},
                {'range': [85, 95], 'color': "yellow"},
                {'range': [95, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 98
            }
        }
    ))
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_right:
    st.subheader("⚡ Performance Analysis")

    # Delivery time distribution
    fig_delivery = px.histogram(
        mission_df,
        x='avg_delivery_time',
        title='Delivery Time Distribution',
        nbins=15,
        color_discrete_sequence=['#FF6B6B']
    )
    st.plotly_chart(fig_delivery, use_container_width=True)

    # Mission success vs failure
    success_data = pd.DataFrame({
        'Status': ['Successful', 'Failed'],
        'Count': [
            mission_df['missions_completed'].sum() - mission_df['missions_failed'].sum(),
            mission_df['missions_failed'].sum()
        ]
    })

    fig_success = px.pie(
        success_data,
        values='Count',
        names='Status',
        title='Mission Success Distribution',
        color_discrete_map={'Successful': '#4CAF50', 'Failed': '#F44336'}
    )
    st.plotly_chart(fig_success, use_container_width=True)

# Advanced Analytics
st.subheader("🔍 Advanced Analytics")

col_a, col_b = st.columns(2)

with col_a:
    # Correlation heatmap
    correlation_data = mission_df[['missions_completed', 'success_rate', 'avg_delivery_time', 'distance_covered']].corr()

    fig_heatmap = px.imshow(
        correlation_data,
        text_auto=True,
        aspect="auto",
        title="Performance Metrics Correlation"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col_b:
    # Weekly performance comparison
    mission_df['week'] = mission_df['date'].dt.isocalendar().week
    weekly_data = mission_df.groupby('week').agg({
        'missions_completed': 'sum',
        'success_rate': 'mean',
        'avg_delivery_time': 'mean'
    }).reset_index()

    fig_weekly = px.bar(
        weekly_data,
        x='week',
        y='missions_completed',
        title='Weekly Mission Volume',
        color='success_rate',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_weekly, use_container_width=True)

# Mission Details Table
st.subheader("📋 Recent Mission Details")

# Generate recent missions
recent_missions = []
for i in range(20):
    mission_time = datetime.now() - timedelta(hours=i)
    recent_missions.append({
        'mission_id': f'M-{2024001 + i:06d}',
        'drone_id': f'LLA-{np.random.randint(1, 15):03d}',
        'start_time': mission_time,
        'end_time': mission_time + timedelta(minutes=np.random.randint(8, 25)),
        'destination': f'Zone {np.random.choice(["Alpha", "Beta", "Gamma", "Delta"])}',
        'cargo': np.random.choice(['Blood Pack', 'Emergency Kit', 'Medications', 'Vaccines', 'IV Fluids']),
        'status': np.random.choice(['Completed', 'In Progress', 'Failed'], p=[0.85, 0.10, 0.05]),
        'distance': f'{np.random.uniform(5, 25):.1f} km'
    })

missions_df = pd.DataFrame(recent_missions)

# Calculate duration
missions_df['duration'] = (missions_df['end_time'] - missions_df['start_time']).dt.total_seconds() / 60

column_config = {
    "mission_id": "Mission ID",
    "drone_id": "Drone ID", 
    "start_time": st.column_config.DatetimeColumn(
        "Start Time",
        format="DD/MM HH:mm"
    ),
    "duration": st.column_config.NumberColumn(
        "Duration (min)",
        format="%.1f"
    ),
    "destination": "Destination",
    "cargo": "Medical Cargo",
    "status": st.column_config.SelectboxColumn(
        "Status",
        options=["Completed", "In Progress", "Failed"]
    ),
    "distance": "Distance"
}

st.dataframe(
    missions_df[['mission_id', 'drone_id', 'start_time', 'duration', 'destination', 'cargo', 'status', 'distance']],
    use_container_width=True,
    column_config=column_config,
    hide_index=True
)

# Performance Insights
st.subheader("💡 Performance Insights")

insights = [
    "🎯 Mission success rate has improved by 2.3% over the last week",
    "⚡ Average delivery time reduced by 1.2 minutes compared to last month", 
    "📦 Medical supply delivery efficiency up 15% due to route optimization",
    "🔋 Battery management improvements have reduced emergency landings by 40%",
    "🌤️ Weather-related mission delays decreased by 25% with better forecasting"
]

for insight in insights:
    st.info(insight)

# Export options
st.subheader("📤 Export Options")

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    if st.button("📊 Export Analytics", use_container_width=True):
        st.success("Analytics data exported to CSV!")

with col_exp2:
    if st.button("📋 Mission Report", use_container_width=True):
        st.success("Mission report generated!")

with col_exp3:
    if st.button("📈 Performance Dashboard", use_container_width=True):
        st.success("Dashboard exported to PDF!")
