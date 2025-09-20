import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Maintenance", page_icon="🔧", layout="wide")

st.title("🔧 Drone Maintenance & Diagnostics")
st.markdown("Comprehensive maintenance tracking and predictive analytics for VTOL medical drone fleet")

# Generate maintenance data
def generate_maintenance_data():
    drone_ids = [f'LLA-{i:03d}' for i in range(1, 16)]
    components = ['Rotors', 'Battery', 'GPS Module', 'Camera', 'Communication', 'Landing Gear', 'Cargo Bay', 'Flight Controller']

    maintenance_records = []
    for drone_id in drone_ids:
        for component in components:
            health_score = np.random.uniform(60, 100)
            last_service = datetime.now() - timedelta(days=np.random.randint(1, 180))
            next_service = last_service + timedelta(days=np.random.randint(30, 90))

            maintenance_records.append({
                'drone_id': drone_id,
                'component': component,
                'health_score': health_score,
                'status': 'Critical' if health_score < 70 else 'Warning' if health_score < 85 else 'Good',
                'last_service': last_service,
                'next_service': next_service,
                'flight_hours': np.random.uniform(0, 500),
                'cycles': np.random.randint(0, 1000),
                'failure_probability': max(0, (100 - health_score) / 100),
                'estimated_cost': np.random.uniform(100, 2000),
                'technician': np.random.choice(['Tech-A', 'Tech-B', 'Tech-C', 'Tech-D']),
                'priority': np.random.choice(['High', 'Medium', 'Low'])
            })

    return pd.DataFrame(maintenance_records)

maintenance_df = generate_maintenance_data()

# Fleet Health Overview
st.subheader("🏥 Fleet Health Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_health = maintenance_df['health_score'].mean()
    st.metric("🎯 Avg Fleet Health", f"{avg_health:.1f}%", f"+{np.random.uniform(0.5, 2.0):.1f}%")

with col2:
    critical_components = len(maintenance_df[maintenance_df['status'] == 'Critical'])
    st.metric("🚨 Critical Components", critical_components, f"-{np.random.randint(1, 3)}")

with col3:
    overdue_maintenance = len(maintenance_df[maintenance_df['next_service'] < datetime.now()])
    st.metric("⏰ Overdue Maintenance", overdue_maintenance)

with col4:
    total_flight_hours = maintenance_df['flight_hours'].sum()
    st.metric("✈️ Total Flight Hours", f"{total_flight_hours:.0f}h", f"+{np.random.randint(10, 50)}h")

with col5:
    estimated_costs = maintenance_df[maintenance_df['status'].isin(['Critical', 'Warning'])]['estimated_cost'].sum()
    st.metric("💰 Est. Repair Costs", f"${estimated_costs:.0f}", f"+${np.random.randint(200, 800)}")

# Main maintenance dashboard
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🔍 Component Health Analysis")

    # Component health heatmap
    pivot_df = maintenance_df.pivot_table(
        index='drone_id', 
        columns='component', 
        values='health_score', 
        aggfunc='mean'
    )

    fig_heatmap = px.imshow(
        pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale='RdYlGn',
        title="Component Health Heatmap",
        labels={'color': 'Health Score (%)'}
    )
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Maintenance schedule timeline
    st.subheader("📅 Maintenance Schedule")

    # Filter for upcoming maintenance
    upcoming_maintenance = maintenance_df[
        (maintenance_df['next_service'] >= datetime.now()) & 
        (maintenance_df['next_service'] <= datetime.now() + timedelta(days=30))
    ].sort_values('next_service')

    if not upcoming_maintenance.empty:
        for _, record in upcoming_maintenance.head(10).iterrows():
            days_until = (record['next_service'] - datetime.now()).days
            urgency_color = '#f44336' if days_until <= 3 else '#ff9800' if days_until <= 7 else '#4caf50'

            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; border-left: 4px solid {urgency_color}; background: #f5f5f5; border-radius: 5px;">
                <strong>{record['drone_id']} - {record['component']}</strong><br>
                Due: {record['next_service'].strftime('%Y-%m-%d')} ({days_until} days)<br>
                Health Score: {record['health_score']:.1f}% | Priority: {record['priority']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No maintenance scheduled for the next 30 days")

with col_right:
    st.subheader("🚨 Critical Alerts")

    # Critical components needing immediate attention
    critical_alerts = maintenance_df[maintenance_df['status'] == 'Critical'].sort_values('health_score')

    if not critical_alerts.empty:
        for _, alert in critical_alerts.head(8).iterrows():
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background: #ffebee; border: 1px solid #f44336; border-radius: 5px;">
                <strong style="color: #f44336;">🚨 {alert['drone_id']}</strong><br>
                Component: {alert['component']}<br>
                Health: {alert['health_score']:.1f}%<br>
                Flight Hours: {alert['flight_hours']:.1f}h<br>
                Technician: {alert['technician']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical maintenance alerts")

    st.subheader("⚠️ Warnings")
    warning_alerts = maintenance_df[maintenance_df['status'] == 'Warning'].sort_values('health_score')

    if not warning_alerts.empty:
        for _, warning in warning_alerts.head(5).iterrows():
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background: #fff3e0; border: 1px solid #ff9800; border-radius: 5px;">
                <strong style="color: #ff9800;">⚠️ {warning['drone_id']}</strong><br>
                Component: {warning['component']}<br>
                Health: {warning['health_score']:.1f}%<br>
                Next Service: {warning['next_service'].strftime('%Y-%m-%d')}
            </div>
            """, unsafe_allow_html=True)

# Detailed maintenance table
st.subheader("📋 Detailed Maintenance Records")

# Filters
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    drone_filter = st.selectbox("Filter by Drone", ['All'] + list(maintenance_df['drone_id'].unique()))

with col_f2:
    component_filter = st.selectbox("Filter by Component", ['All'] + list(maintenance_df['component'].unique()))

with col_f3:
    status_filter = st.selectbox("Filter by Status", ['All', 'Critical', 'Warning', 'Good'])

# Apply filters
filtered_maintenance = maintenance_df.copy()

if drone_filter != 'All':
    filtered_maintenance = filtered_maintenance[filtered_maintenance['drone_id'] == drone_filter]

if component_filter != 'All':
    filtered_maintenance = filtered_maintenance[filtered_maintenance['component'] == component_filter]

if status_filter != 'All':
    filtered_maintenance = filtered_maintenance[filtered_maintenance['status'] == status_filter]

# Configure table columns
column_config = {
    "drone_id": "Drone ID",
    "component": "Component",
    "health_score": st.column_config.ProgressColumn(
        "Health Score",
        min_value=0,
        max_value=100,
        format="%.1f%%"
    ),
    "status": st.column_config.SelectboxColumn(
        "Status",
        options=["Critical", "Warning", "Good"]
    ),
    "flight_hours": st.column_config.NumberColumn(
        "Flight Hours",
        format="%.1f h"
    ),
    "cycles": "Cycles",
    "failure_probability": st.column_config.ProgressColumn(
        "Failure Risk",
        min_value=0,
        max_value=1,
        format="%.1f%%"
    ),
    "next_service": st.column_config.DateColumn("Next Service"),
    "estimated_cost": st.column_config.NumberColumn(
        "Est. Cost",
        format="$%.0f"
    ),
    "technician": "Technician",
    "priority": st.column_config.SelectboxColumn(
        "Priority",
        options=["High", "Medium", "Low"]
    )
}

st.dataframe(
    filtered_maintenance,
    use_container_width=True,
    column_config=column_config,
    hide_index=True
)

# Analytics and Insights
st.subheader("📊 Maintenance Analytics")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Component health distribution
    component_health = maintenance_df.groupby('component')['health_score'].mean().sort_values(ascending=True)

    fig_component = px.bar(
        x=component_health.values,
        y=component_health.index,
        orientation='h',
        title="Average Component Health Scores",
        color=component_health.values,
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_component, use_container_width=True)

with col_chart2:
    # Flight hours vs health score correlation
    fig_scatter = px.scatter(
        maintenance_df,
        x='flight_hours',
        y='health_score',
        color='component',
        title='Flight Hours vs Health Score',
        hover_data=['drone_id', 'status']
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Predictive maintenance insights
col_pred1, col_pred2 = st.columns(2)

with col_pred1:
    # Failure probability by component
    failure_prob = maintenance_df.groupby('component')['failure_probability'].mean().sort_values(ascending=False)

    fig_failure = px.bar(
        x=failure_prob.index,
        y=failure_prob.values,
        title="Component Failure Probability",
        color=failure_prob.values,
        color_continuous_scale='Reds'
    )
    fig_failure.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_failure, use_container_width=True)

with col_pred2:
    # Maintenance cost trends
    cost_by_status = maintenance_df.groupby('status')['estimated_cost'].sum()

    fig_cost = px.pie(
        values=cost_by_status.values,
        names=cost_by_status.index,
        title="Estimated Repair Costs by Status",
        color_discrete_map={
            'Critical': '#f44336',
            'Warning': '#ff9800',
            'Good': '#4caf50'
        }
    )
    st.plotly_chart(fig_cost, use_container_width=True)

# Maintenance Actions
st.subheader("🛠️ Maintenance Actions")

col_act1, col_act2, col_act3, col_act4 = st.columns(4)

with col_act1:
    if st.button("📋 Schedule Maintenance", use_container_width=True):
        st.success("Maintenance scheduling interface opened!")

with col_act2:
    if st.button("🔧 Log Repair", use_container_width=True):
        st.info("Repair logging system activated!")

with col_act3:
    if st.button("📊 Generate Report", use_container_width=True):
        st.success("Maintenance report generated!")

with col_act4:
    if st.button("⚠️ Emergency Inspection", use_container_width=True):
        st.warning("Emergency inspection protocol initiated!")

# Maintenance team dashboard
st.subheader("👥 Maintenance Team Status")

col_team1, col_team2 = st.columns(2)

with col_team1:
    # Technician workload
    tech_workload = maintenance_df[maintenance_df['status'].isin(['Critical', 'Warning'])].groupby('technician').size()

    fig_workload = px.bar(
        x=tech_workload.index,
        y=tech_workload.values,
        title="Technician Workload (Critical & Warning Items)",
        color=tech_workload.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_workload, use_container_width=True)

with col_team2:
    # Team performance metrics
    team_metrics = pd.DataFrame({
        'Technician': ['Tech-A', 'Tech-B', 'Tech-C', 'Tech-D'],
        'Completed_Jobs': [23, 31, 28, 19],
        'Avg_Repair_Time': [2.5, 1.8, 2.1, 2.9],
        'Success_Rate': [94, 97, 91, 89]
    })

    fig_performance = px.scatter(
        team_metrics,
        x='Avg_Repair_Time',
        y='Success_Rate',
        size='Completed_Jobs',
        text='Technician',
        title='Team Performance Analysis',
        labels={'Avg_Repair_Time': 'Avg Repair Time (hours)', 'Success_Rate': 'Success Rate (%)'}
    )
    fig_performance.update_traces(textposition="top center")
    st.plotly_chart(fig_performance, use_container_width=True)

# Sidebar maintenance controls
with st.sidebar:
    st.subheader("🔧 Maintenance Controls")

    # Quick maintenance log
    with st.form("maintenance_log"):
        st.write("**Quick Maintenance Log**")
        log_drone = st.selectbox("Drone", maintenance_df['drone_id'].unique())
        log_component = st.selectbox("Component", maintenance_df['component'].unique())
        log_action = st.text_area("Action Taken")
        log_technician = st.selectbox("Technician", ['Tech-A', 'Tech-B', 'Tech-C', 'Tech-D'])

        if st.form_submit_button("Log Maintenance"):
            if log_action:
                st.success(f"Maintenance logged for {log_drone}!")

    st.subheader("📊 Quick Stats")
    overdue_count = len(maintenance_df[maintenance_df['next_service'] < datetime.now()])
    st.metric("Overdue Items", overdue_count)

    critical_count = len(maintenance_df[maintenance_df['status'] == 'Critical'])
    st.metric("Critical Items", critical_count)

    avg_health_all = maintenance_df['health_score'].mean()
    st.metric("Fleet Health", f"{avg_health_all:.1f}%")
