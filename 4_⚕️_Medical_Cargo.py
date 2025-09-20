import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Medical Cargo", page_icon="⚕️", layout="wide")

st.title("⚕️ Medical Cargo Management")
st.markdown("Advanced medical supply tracking and inventory management system")

# Generate medical inventory data
def generate_medical_inventory():
    medical_items = [
        {'category': 'Blood Products', 'items': ['O+ Blood Pack', 'O- Blood Pack', 'A+ Blood Pack', 'A- Blood Pack', 'B+ Blood Pack', 'AB+ Blood Pack']},
        {'category': 'Emergency Medications', 'items': ['Epinephrine', 'Morphine', 'Atropine', 'Naloxone', 'Adenosine', 'Amiodarone']},
        {'category': 'IV Fluids', 'items': ['Normal Saline', 'Lactated Ringers', 'D5W', 'Plasma Expander']},
        {'category': 'Surgical Supplies', 'items': ['Trauma Kit', 'Suture Kit', 'Emergency Airway Kit', 'Chest Tube Kit']},
        {'category': 'Vaccines', 'items': ['COVID-19 Vaccine', 'Hepatitis B', 'Tetanus Toxoid', 'Rabies Vaccine']},
        {'category': 'Equipment', 'items': ['Portable Defibrillator', 'Oxygen Tank', 'Blood Glucose Monitor', 'Thermometer']}
    ]

    inventory = []
    for cat in medical_items:
        for item in cat['items']:
            inventory.append({
                'item_id': f"MED-{len(inventory)+1:04d}",
                'category': cat['category'],
                'item_name': item,
                'current_stock': np.random.randint(5, 100),
                'min_stock': np.random.randint(10, 25),
                'max_stock': np.random.randint(80, 150),
                'temperature_req': np.random.choice(['2-8°C', 'Room Temp', '-20°C']),
                'expiry_date': datetime.now() + timedelta(days=np.random.randint(30, 730)),
                'priority': np.random.choice(['Critical', 'High', 'Medium', 'Low']),
                'location': f"Storage Unit {np.random.choice(['A', 'B', 'C', 'D'])}",
                'batch_number': f"BT{np.random.randint(1000, 9999)}",
                'supplier': np.random.choice(['MedCorp', 'HealthSupply Inc', 'BioTech Ltd', 'MediCore']),
                'cost_per_unit': np.random.uniform(10, 500)
            })

    return pd.DataFrame(inventory)

inventory_df = generate_medical_inventory()

# Calculate stock status
def get_stock_status(row):
    if row['current_stock'] <= row['min_stock']:
        return 'Critical'
    elif row['current_stock'] <= row['min_stock'] * 1.5:
        return 'Low'
    elif row['current_stock'] >= row['max_stock'] * 0.8:
        return 'Overstocked'
    else:
        return 'Normal'

inventory_df['stock_status'] = inventory_df.apply(get_stock_status, axis=1)

# Calculate days until expiry
inventory_df['days_to_expiry'] = (inventory_df['expiry_date'] - datetime.now()).dt.days

# Inventory Overview Dashboard
st.subheader("📊 Inventory Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_items = len(inventory_df)
    st.metric("📦 Total Items", total_items)

with col2:
    critical_stock = len(inventory_df[inventory_df['stock_status'] == 'Critical'])
    st.metric("🚨 Critical Stock", critical_stock, delta=f"-{np.random.randint(1, 5)}")

with col3:
    expiring_soon = len(inventory_df[inventory_df['days_to_expiry'] <= 30])
    st.metric("⏰ Expiring Soon", expiring_soon)

with col4:
    total_value = inventory_df['current_stock'] * inventory_df['cost_per_unit']
    st.metric("💰 Total Value", f"${total_value.sum():,.0f}")

with col5:
    avg_stock_level = (inventory_df['current_stock'] / inventory_df['max_stock'] * 100).mean()
    st.metric("📈 Avg Stock Level", f"{avg_stock_level:.0f}%")

# Main dashboard layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📋 Medical Inventory Details")

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        category_filter = st.selectbox(
            "Filter by Category",
            ['All'] + list(inventory_df['category'].unique())
        )

    with col_f2:
        priority_filter = st.selectbox(
            "Filter by Priority", 
            ['All'] + list(inventory_df['priority'].unique())
        )

    with col_f3:
        status_filter = st.selectbox(
            "Filter by Stock Status",
            ['All'] + list(inventory_df['stock_status'].unique())
        )

    # Apply filters
    filtered_df = inventory_df.copy()

    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category_filter]

    if priority_filter != 'All':
        filtered_df = filtered_df[filtered_df['priority'] == priority_filter]

    if status_filter != 'All':
        filtered_df = filtered_df[filtered_df['stock_status'] == status_filter]

    # Configure table columns
    column_config = {
        "item_id": "Item ID",
        "category": "Category",
        "item_name": "Item Name",
        "current_stock": st.column_config.NumberColumn(
            "Current Stock",
            format="%d units"
        ),
        "stock_status": st.column_config.SelectboxColumn(
            "Status",
            options=["Critical", "Low", "Normal", "Overstocked"]
        ),
        "temperature_req": "Temperature",
        "days_to_expiry": st.column_config.NumberColumn(
            "Days to Expiry",
            format="%d days"
        ),
        "priority": st.column_config.SelectboxColumn(
            "Priority",
            options=["Critical", "High", "Medium", "Low"]
        ),
        "location": "Location",
        "cost_per_unit": st.column_config.NumberColumn(
            "Unit Cost",
            format="$%.2f"
        )
    }

    # Display inventory table
    st.dataframe(
        filtered_df[[
            'item_id', 'category', 'item_name', 'current_stock', 
            'stock_status', 'temperature_req', 'days_to_expiry', 
            'priority', 'location', 'cost_per_unit'
        ]],
        use_container_width=True,
        column_config=column_config,
        hide_index=True
    )

with col_right:
    st.subheader("🚨 Critical Alerts")

    # Critical stock items
    critical_items = inventory_df[inventory_df['stock_status'] == 'Critical']

    if not critical_items.empty:
        for _, item in critical_items.head(5).iterrows():
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background: #ffebee; border: 1px solid #f44336; border-radius: 5px;">
                <strong style="color: #f44336;">🚨 {item['item_name']}</strong><br>
                Stock: {item['current_stock']} units<br>
                Min Required: {item['min_stock']} units<br>
                Location: {item['location']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical stock alerts")

    # Expiring items
    st.subheader("⏰ Expiring Items")
    expiring_items = inventory_df[inventory_df['days_to_expiry'] <= 30].sort_values('days_to_expiry')

    if not expiring_items.empty:
        for _, item in expiring_items.head(5).iterrows():
            color = "#f44336" if item['days_to_expiry'] <= 7 else "#ff9800"
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background: #fff3e0; border: 1px solid {color}; border-radius: 5px;">
                <strong style="color: {color};">⏰ {item['item_name']}</strong><br>
                Expires in: {item['days_to_expiry']} days<br>
                Batch: {item['batch_number']}<br>
                Stock: {item['current_stock']} units
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No items expiring soon")

# Analytics and Charts
st.subheader("📈 Inventory Analytics")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Stock status distribution
    status_counts = inventory_df['stock_status'].value_counts()

    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Stock Status Distribution",
        color_discrete_map={
            'Critical': '#f44336',
            'Low': '#ff9800',
            'Normal': '#4caf50',
            'Overstocked': '#2196f3'
        }
    )
    st.plotly_chart(fig_status, use_container_width=True)

with col_chart2:
    # Category distribution
    category_counts = inventory_df['category'].value_counts()

    fig_category = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="Items by Category",
        color=category_counts.values,
        color_continuous_scale='Viridis'
    )
    fig_category.update_layout(xaxis_title="Category", yaxis_title="Number of Items")
    st.plotly_chart(fig_category, use_container_width=True)

# Temperature requirements
col_temp1, col_temp2 = st.columns(2)

with col_temp1:
    # Temperature requirements
    temp_counts = inventory_df['temperature_req'].value_counts()

    fig_temp = px.pie(
        values=temp_counts.values,
        names=temp_counts.index,
        title="Temperature Requirements"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col_temp2:
    # Priority distribution
    priority_counts = inventory_df['priority'].value_counts()

    fig_priority = px.funnel(
        x=priority_counts.values,
        y=priority_counts.index,
        title="Priority Distribution"
    )
    st.plotly_chart(fig_priority, use_container_width=True)

# Active Deliveries Section
st.subheader("🚚 Active Medical Deliveries")

# Generate active delivery data
def generate_active_deliveries():
    deliveries = []
    for i in range(8):
        start_time = datetime.now() - timedelta(minutes=np.random.randint(5, 60))
        deliveries.append({
            'delivery_id': f'DEL-{2024000 + i:06d}',
            'drone_id': f'LLA-{np.random.randint(1, 15):03d}',
            'medical_item': np.random.choice(inventory_df['item_name'].tolist()),
            'quantity': np.random.randint(1, 10),
            'destination': f'Medical Station {chr(65 + np.random.randint(0, 5))}',
            'priority': np.random.choice(['Critical', 'High', 'Medium']),
            'status': np.random.choice(['In Transit', 'Delivered', 'Loading'], p=[0.6, 0.3, 0.1]),
            'start_time': start_time,
            'eta': start_time + timedelta(minutes=np.random.randint(10, 45)),
            'temperature_status': np.random.choice(['Normal', 'Alert'], p=[0.9, 0.1]),
            'gps_status': 'Active',
            'chain_of_custody': 'Verified'
        })

    return pd.DataFrame(deliveries)

deliveries_df = generate_active_deliveries()

# Display active deliveries
delivery_column_config = {
    "delivery_id": "Delivery ID",
    "drone_id": "Drone ID",
    "medical_item": "Medical Item", 
    "quantity": "Quantity",
    "destination": "Destination",
    "priority": st.column_config.SelectboxColumn(
        "Priority",
        options=["Critical", "High", "Medium", "Low"]
    ),
    "status": st.column_config.SelectboxColumn(
        "Status", 
        options=["In Transit", "Delivered", "Loading", "Delayed"]
    ),
    "start_time": st.column_config.DatetimeColumn(
        "Start Time",
        format="HH:mm"
    ),
    "eta": st.column_config.DatetimeColumn(
        "ETA",
        format="HH:mm"
    ),
    "temperature_status": "Temp Status"
}

st.dataframe(
    deliveries_df,
    use_container_width=True,
    column_config=delivery_column_config,
    hide_index=True
)

# Quick Actions
st.subheader("⚡ Quick Actions")

col_act1, col_act2, col_act3, col_act4 = st.columns(4)

with col_act1:
    if st.button("📦 New Delivery", use_container_width=True):
        st.success("New delivery request initiated!")

with col_act2:
    if st.button("📊 Generate Report", use_container_width=True):
        st.info("Inventory report generated!")

with col_act3:
    if st.button("🔄 Refresh Inventory", use_container_width=True):
        st.rerun()

with col_act4:
    if st.button("⚠️ Emergency Restock", use_container_width=True):
        st.warning("Emergency restock protocol activated!")

# Sidebar controls
with st.sidebar:
    st.subheader("📋 Inventory Controls")

    # Add new item form
    with st.form("add_item"):
        st.write("**Add New Item**")
        new_category = st.selectbox("Category", inventory_df['category'].unique())
        new_item = st.text_input("Item Name")
        new_quantity = st.number_input("Initial Stock", min_value=0, max_value=1000)
        new_priority = st.selectbox("Priority", ['Critical', 'High', 'Medium', 'Low'])

        if st.form_submit_button("Add Item"):
            if new_item:
                st.success(f"Added {new_item} to inventory!")

    st.subheader("🔍 Search & Filters")
    search_term = st.text_input("Search items...")

    if search_term:
        search_results = inventory_df[
            inventory_df['item_name'].str.contains(search_term, case=False, na=False)
        ]
        st.write(f"Found {len(search_results)} items")

    st.subheader("📈 Quick Stats")
    st.metric("Low Stock Items", len(inventory_df[inventory_df['stock_status'].isin(['Critical', 'Low'])]))
    st.metric("Total Categories", inventory_df['category'].nunique())
    st.metric("Avg Days to Expiry", f"{inventory_df['days_to_expiry'].mean():.0f}")
