import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Smart Microgrid - Power Equalization System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<div class="main-header">⚡ Smart Microgrid Power Equalization System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Berbasis Frekuensi Radio Sub-Gigahertz untuk Kawasan Nirinternet</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ System Configuration")
    
    if 'prev_num_houses' not in st.session_state:
        st.session_state.prev_num_houses = 8
    
    num_houses = st.slider("Number of Houses", 3, 20, 8)
    
    if num_houses != st.session_state.prev_num_houses:
        st.session_state.prev_num_houses = num_houses
        st.session_state.houses = []
        st.session_state.initialized = False
    
    st.subheader("📡 Communication Settings")
    frequency = st.selectbox(
        "Radio Frequency Band",
        ["433 MHz", "868 MHz", "915 MHz", "2.4 GHz"]
    )
    range_km = st.slider("Communication Range (km)", 0.5, 10.0, 3.0)
    
    st.subheader("⚡ Power Parameters")
    base_load = st.slider("Base Load per House (W)", 100, 500, 250)
    solar_capacity = st.slider("Solar Panel Capacity (W)", 200, 1000, 500)
    battery_capacity = st.slider("Battery Capacity (kWh)", 1, 10, 5)
    
    st.subheader("🤖 Algorithm Settings")
    # TAMBAHKAN: Threshold yang bisa diatur
    equalization_threshold = st.slider("Equalization Threshold (W)", 10, 100, 30, 
                                       help="Minimal selisih daya untuk menentukan surplus/defisit")
    update_interval = st.number_input("Update Interval (seconds)", 1, 10, 3)

# Initialize session state with parameters
if 'initialized' not in st.session_state or not st.session_state.initialized:
    st.session_state.houses = []
    for i in range(num_houses):
        load_variation = random.randint(-50, 50)
        solar_variation = random.randint(-50, 50)
        
        st.session_state.houses.append({
            'id': i,
            'name': f'House {i+1}',
            'load': base_load + load_variation,
            'solar': solar_capacity + solar_variation,
            'battery': random.randint(20, 90),
            'battery_capacity': battery_capacity,
            'status': 'normal',
            'power_balance': 0,
            'surplus': False,
            'deficit': False,
            'role': 'idle'
        })
    st.session_state.initialized = True

# Function to update power data with parameters
def update_power_data():
    base_load = st.session_state.get('base_load', 250)
    solar_capacity = st.session_state.get('solar_capacity', 500)
    battery_capacity = st.session_state.get('battery_capacity', 5)
    # Ambil threshold dari session state
    threshold = st.session_state.get('equalization_threshold', 30)
    
    for house in st.session_state.houses:
        load_change = random.randint(-30, 30)
        solar_change = random.randint(-30, 30)
        battery_change = random.randint(-5, 5)
        
        new_load = base_load + load_change
        house['load'] = max(50, new_load)
        
        new_solar = solar_capacity + solar_change
        house['solar'] = max(0, new_solar)
        
        new_battery = house['battery'] + battery_change
        house['battery'] = max(0, min(100, new_battery))
        
        house['battery_capacity'] = battery_capacity
        
        # Calculate power balance
        house['power_balance'] = house['solar'] - house['load']
        
        # PERBAIKAN: Gunakan threshold yang bisa diatur
        house['surplus'] = house['power_balance'] > threshold
        house['deficit'] = house['power_balance'] < -threshold
        
        # Determine role
        if house['surplus'] and house['battery'] > 20:
            house['role'] = 'supplier'
        elif house['deficit'] and house['battery'] < 90:
            house['role'] = 'consumer'
        else:
            house['role'] = 'idle'

# Simpan parameter ke session state
st.session_state.base_load = base_load
st.session_state.solar_capacity = solar_capacity
st.session_state.battery_capacity = battery_capacity
st.session_state.equalization_threshold = equalization_threshold

# Real-time update button
if st.button("🔄 Update Power Data"):
    update_power_data()

# Auto-update
if st.checkbox("Enable Auto-Update"):
    placeholder = st.empty()
    while True:
        update_power_data()
        time.sleep(update_interval)
        break

# Main Dashboard
col1, col2, col3 = st.columns(3)

# Statistics
total_load = sum(h['load'] for h in st.session_state.houses)
total_solar = sum(h['solar'] for h in st.session_state.houses)
total_balance = total_solar - total_load
surplus_houses = sum(1 for h in st.session_state.houses if h['surplus'])
deficit_houses = sum(1 for h in st.session_state.houses if h['deficit'])

with col1:
    st.metric("Total Load", f"{total_load:.0f} W", delta="Demand")
    st.metric("Total Solar Generation", f"{total_solar:.0f} W", delta="Supply")

with col2:
    st.metric("Network Balance", f"{total_balance:.0f} W", 
              delta="Surplus" if total_balance > 0 else "Deficit",
              delta_color="normal")
    st.metric("Active Houses", f"{len(st.session_state.houses)}", delta="Connected")

with col3:
    st.metric("Surplus Houses", f"{surplus_houses}", delta="⚡ Extra Power")
    st.metric("Deficit Houses", f"{deficit_houses}", delta="🔋 Need Power")

# Communication Network Visualization
st.subheader("📡 Sub-GHz Communication Network")
col1, col2 = st.columns([3, 1])

with col1:
    fig = go.Figure()
    
    n = len(st.session_state.houses)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    radius = 3
    
    for i in range(n):
        for j in range(i+1, n):
            if random.random() > 0.3:
                x0, y0 = radius * np.cos(angles[i]), radius * np.sin(angles[i])
                x1, y1 = radius * np.cos(angles[j]), radius * np.sin(angles[j])
                fig.add_trace(go.Scatter(
                    x=[x0, x1], y=[y0, y1],
                    mode='lines',
                    line=dict(width=1, color='lightgray'),
                    showlegend=False,
                    hoverinfo='none'
                ))
    
    for i, house in enumerate(st.session_state.houses):
        x, y = radius * np.cos(angles[i]), radius * np.sin(angles[i])
        color = 'green' if house['surplus'] else 'red' if house['deficit'] else 'blue'
        size = 20 + abs(house['power_balance']) / 10
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=size, color=color, line=dict(width=2, color='white')),
            text=[f"{house['name']}<br>{house['power_balance']:.0f}W"],
            textposition='top center',
            name=house['name'],
            hovertemplate=f"<b>{house['name']}</b><br>"
                         f"Load: {house['load']:.0f} W<br>"
                         f"Solar: {house['solar']:.0f} W<br>"
                         f"Battery: {house['battery']:.0f}%<br>"
                         f"Role: {house['role']}<extra></extra>"
        ))
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        title_text="Network Topology & Power Flow"
    )
    
    st.plotly_chart(fig, width='stretch')

with col2:
    st.info("📡 **Communication Protocol**")
    st.markdown(f"""
    - **Frequency:** {frequency}
    - **Range:** {range_km} km
    - **Network Type:** Mesh
    - **Protocol:** LoRa/LoRaWAN
    - **Data Rate:** Adaptive
    - **Latency:** < 100ms
    """)
    
    st.success("🤖 **Power Equalization Algorithm**")
    st.markdown(f"""
    - **Threshold:** {equalization_threshold} W
    - **Method:** Distributed Consensus
    - **Priority:** Battery Level
    - **Efficiency:** 92%
    """)

# House Status Table
st.subheader("🏠 House Status Dashboard")

df = pd.DataFrame(st.session_state.houses)
df_display = df[['name', 'load', 'solar', 'battery', 'battery_capacity', 'power_balance', 'role', 'status']].copy()
df_display['power_balance'] = df_display['power_balance'].round(1)
df_display['battery'] = df_display['battery'].round(1)

def color_role(val):
    colors = {
        'supplier': 'background-color: #90EE90;',
        'consumer': 'background-color: #F08080;',
        'idle': 'background-color: #D3D3D3;'
    }
    return colors.get(val, '')

styled_df = df_display.style.map(color_role, subset=['role'])
st.dataframe(styled_df, width='stretch')

# Power Flow Visualization
st.subheader("⚡ Real-time Power Flow")

fig_power = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Power Balance", "Battery Status", "Solar vs Load", "Network Health")
)

balance_values = [h['power_balance'] for h in st.session_state.houses]
colors = ['green' if v > 0 else 'red' if v < 0 else 'blue' for v in balance_values]
fig_power.add_trace(
    go.Bar(
        x=[h['name'] for h in st.session_state.houses],
        y=balance_values,
        marker_color=colors,
        name="Balance"
    ),
    row=1, col=1
)

fig_power.add_trace(
    go.Bar(
        x=[h['name'] for h in st.session_state.houses],
        y=[h['battery'] for h in st.session_state.houses],
        marker_color='orange',
        name="Battery %"
    ),
    row=1, col=2
)

fig_power.add_trace(
    go.Bar(
        x=[h['name'] for h in st.session_state.houses],
        y=[h['solar'] for h in st.session_state.houses],
        name="Solar",
        marker_color='gold'
    ),
    row=2, col=1
)
fig_power.add_trace(
    go.Bar(
        x=[h['name'] for h in st.session_state.houses],
        y=[h['load'] for h in st.session_state.houses],
        name="Load",
        marker_color='steelblue'
    ),
    row=2, col=1
)

health_score = [random.randint(70, 98) for _ in st.session_state.houses]
fig_power.add_trace(
    go.Scatter(
        x=[h['name'] for h in st.session_state.houses],
        y=health_score,
        mode='lines+markers',
        name="Network Health",
        line=dict(color='green', width=2)
    ),
    row=2, col=2
)

fig_power.update_layout(height=600, showlegend=True)
st.plotly_chart(fig_power, width='stretch')

# Additional Information
st.subheader("📊 System Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    **🔋 Energy Statistics**
    - Total Generated: {total_solar:.0f} W
    - Total Consumed: {total_load:.0f} W
    - Efficiency: {(total_load/total_solar*100 if total_solar > 0 else 0):.1f}%
    """)

with col2:
    st.markdown(f"""
    **📡 Network Status**
    - Active Nodes: {len(st.session_state.houses)}
    - Surplus Nodes: {surplus_houses}
    - Deficit Nodes: {deficit_houses}
    - Network Health: {np.mean(health_score):.1f}%
    """)

with col3:
    st.markdown(f"""
    **⚡ Power Flow**
    - Total Surplus: {sum(h['power_balance'] for h in st.session_state.houses if h['surplus']):.0f} W
    - Total Deficit: {abs(sum(h['power_balance'] for h in st.session_state.houses if h['deficit'])):.0f} W
    - Equalization Threshold: {equalization_threshold} W
    """)

with col4:
    st.markdown(f"""
    **🔧 System Info**
    - Frequency: {frequency}
    - Range: {range_km} km
    - Protocol: LoRa
    - Last Update: {datetime.now().strftime('%H:%M:%S')}
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Smart Microgrid Power Equalization System | Developed for Kawasan Nirinternet
    <br>
    🔬 Research Prototype | Sub-GHz Radio Communication
</div>
""", unsafe_allow_html=True)