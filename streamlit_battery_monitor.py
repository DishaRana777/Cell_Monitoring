import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Battery Cell Monitor Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
        background-size: 300% 300%;
        animation: gradientShift 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .cell-card {
        border-radius: 20px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        color: white;
        font-weight: bold;
        font-family: 'Rajdhani', sans-serif;
        border: 2px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .cell-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }
    
    .cell-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .cell-card:hover::before {
        left: 100%;
    }
    
    .charging {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        animation: chargeGlow 2s ease-in-out infinite alternate;
        box-shadow: 0 0 30px rgba(56, 239, 125, 0.4);
    }
    
    .discharging {
        background: linear-gradient(135deg, #ff416c, #ff4757);
        animation: dischargeGlow 2s ease-in-out infinite alternate;
        box-shadow: 0 0 30px rgba(255, 65, 108, 0.4);
    }
    
    .idle {
        background: linear-gradient(135deg, #4834d4, #686de0);
        box-shadow: 0 0 30px rgba(104, 109, 224, 0.3);
    }
    
    .critical {
        background: linear-gradient(135deg, #e55039, #c44569);
        animation: criticalBlink 1s ease-in-out infinite alternate;
        box-shadow: 0 0 40px rgba(229, 80, 57, 0.6);
    }
    
    @keyframes chargeGlow {
        0% { box-shadow: 0 0 20px rgba(56, 239, 125, 0.4); }
        100% { box-shadow: 0 0 40px rgba(56, 239, 125, 0.8), 0 0 60px rgba(56, 239, 125, 0.4); }
    }
    
    @keyframes dischargeGlow {
        0% { box-shadow: 0 0 20px rgba(255, 65, 108, 0.4); }
        100% { box-shadow: 0 0 40px rgba(255, 65, 108, 0.8), 0 0 60px rgba(255, 65, 108, 0.4); }
    }
    
    @keyframes criticalBlink {
        0% { opacity: 1; }
        100% { opacity: 0.7; }
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 15px 0;
        border: 2px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        font-family: 'Rajdhani', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .metric-container h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    .status-good { 
        color: #2ed573; 
        text-shadow: 0 0 10px rgba(46, 213, 115, 0.5);
        font-weight: bold;
    }
    .status-warning { 
        color: #ffa502; 
        text-shadow: 0 0 10px rgba(255, 165, 2, 0.5);
        font-weight: bold;
    }
    .status-danger { 
        color: #ff3742; 
        text-shadow: 0 0 10px rgba(255, 55, 66, 0.5);
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
        border-radius: 15px;
        padding: 20px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-weight: bold;
        font-family: 'Rajdhani', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .emergency-button {
        background: linear-gradient(135deg, #ff416c, #ff4757) !important;
        animation: pulse 2s infinite;
    }
    
    .emergency-button:hover {
        background: linear-gradient(135deg, #ff4757, #ff416c) !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .neon-text {
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 5px currentColor, 0 0 10px currentColor, 0 0 15px currentColor;
        animation: neonFlicker 3s ease-in-out infinite alternate;
    }
    
    @keyframes neonFlicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .cell-type-nmc {
        border-left: 5px solid #ff6b6b;
    }
    
    .cell-type-lfp {
        border-left: 5px solid #4ecdc4;
    }
    
    .power-positive {
        color: #2ed573;
        font-weight: bold;
    }
    
    .power-negative {
        color: #ff3742;
        font-weight: bold;
    }
    
    .temp-normal { color: #45b7d1; }
    .temp-warm { color: #ffa502; }
    .temp-hot { color: #ff3742; }
    
    .voltage-low { color: #ff3742; }
    .voltage-normal { color: #2ed573; }
    .voltage-high { color: #ffa502; }
</style>
""", unsafe_allow_html=True)

class BatteryMonitor:
    def __init__(self):
        self.cell_params = {
            "LFP": {"nominal": 3.2, "min": 2.8, "max": 3.6},
            "NMC": {"nominal": 3.6, "min": 3.2, "max": 4.0}
        }
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'cells_data' not in st.session_state:
            st.session_state.cells_data = {}
        if 'bench_name' not in st.session_state:
            st.session_state.bench_name = ""
        if 'group_number' not in st.session_state:
            st.session_state.group_number = 1
        if 'historical_data' not in st.session_state:
            st.session_state.historical_data = []
        if 'last_update' not in st.session_state:
            st.session_state.last_update = datetime.now()
        if 'auto_refresh' not in st.session_state:
            st.session_state.auto_refresh = False
            
    def get_cell_status(self, current, voltage, min_v, max_v, temp):
        """Determine cell status based on parameters"""
        if voltage < min_v or voltage > max_v or temp > 50:
            return "critical"
        elif current > 0.1:
            return "charging"
        elif current < -0.1:
            return "discharging"
        else:
            return "idle"
            
    def get_status_color(self, voltage, min_v, max_v, temp):
        """Get status color based on parameters"""
        if voltage < min_v or voltage > max_v or temp > 50:
            return "status-danger"
        elif voltage < min_v * 1.1 or voltage > max_v * 0.9 or temp > 40:
            return "status-warning"
        else:
            return "status-good"
    
    def get_temp_class(self, temp):
        """Get temperature CSS class"""
        if temp > 45:
            return "temp-hot"
        elif temp > 35:
            return "temp-warm"
        else:
            return "temp-normal"
    
    def get_voltage_class(self, voltage, min_v, max_v):
        """Get voltage CSS class"""
        if voltage < min_v * 1.05:
            return "voltage-low"
        elif voltage > max_v * 0.95:
            return "voltage-high"
        else:
            return "voltage-normal"
    
    def get_power_class(self, power):
        """Get power CSS class"""
        if power > 0:
            return "power-positive"
        elif power < 0:
            return "power-negative"
        else:
            return ""

def setup_page():
    """Setup configuration page"""
    st.markdown('<h1 class="main-header">⚙️ Advanced Setup Configuration</h1>', unsafe_allow_html=True)
    
    monitor = BatteryMonitor()
    
    # Create glass card container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏭 Bench Configuration")
        bench_name = st.text_input("🏷️ Bench Name", value=st.session_state.get('bench_name', ''), 
                                  placeholder="Enter your bench identifier")
        group_number = st.number_input("👥 Group Number", min_value=1, max_value=100, 
                                     value=st.session_state.get('group_number', 1))
        
        st.markdown("### 🔋 Cell Configuration")
        num_cells = st.number_input("📊 Number of Cells", min_value=1, max_value=16, value=8)
        
    with col2:
        st.markdown("### 🔧 Individual Cell Setup")
        cells_config = []
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        
        for i in range(num_cells):
            col_inner1, col_inner2 = st.columns([3, 1])
            with col_inner1:
                cell_type = st.selectbox(f"🔋 Cell {i+1} Type", ["LFP", "NMC"], key=f"cell_type_{i}")
            with col_inner2:
                st.markdown(f'<div style="width:30px;height:30px;background:{colors[i%len(colors)]};border-radius:50%;margin-top:25px;"></div>', 
                           unsafe_allow_html=True)
            cells_config.append(cell_type)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize button with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Initialize Cells", type="primary", use_container_width=True):
            st.session_state.bench_name = bench_name
            st.session_state.group_number = group_number
            
            # Initialize cells
            cells_data = {}
            for idx, cell_type in enumerate(cells_config, start=1):
                cell_key = f"cell_{idx}_{cell_type.lower()}"
                params = monitor.cell_params[cell_type]
                
                cells_data[cell_key] = {
                    "voltage": params["nominal"],
                    "current": 0.0,
                    "temp": round(random.uniform(25, 40), 1),
                    "capacity": 0.0,
                    "total_charge": 0.0,
                    "min_voltage": params["min"],
                    "max_voltage": params["max"],
                    "cell_type": cell_type,
                    "status": "idle",
                    "health": "good",
                    "color": colors[idx % len(colors)]
                }
            
            st.session_state.cells_data = cells_data
            st.balloons()
            st.success(f"✅ Successfully initialized {len(cells_config)} cells!")
            
    # Display initialized cells with enhanced cards
    if st.session_state.cells_data:
        st.markdown("### 🔍 Initialized Cells Overview")
        
        cols = st.columns(4)
        for idx, (key, data) in enumerate(st.session_state.cells_data.items()):
            col = cols[idx % 4]
            
            with col:
                cell_type_class = f"cell-type-{data['cell_type'].lower()}"
                st.markdown(f"""
                <div class="glass-card {cell_type_class}" style="border-left: 5px solid {data.get('color', '#667eea')};">
                    <h4 class="neon-text" style="color: {data.get('color', '#667eea')};">{key.upper()}</h4>
                    <div style="display: flex; justify-content: space-between;">
                        <span>⚡ Voltage:</span>
                        <span class="voltage-normal">{data['voltage']} V</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>🔋 Type:</span>
                        <span style="color: {data.get('color', '#667eea')};">{data['cell_type']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>🌡️ Temp:</span>
                        <span class="temp-normal">{data['temp']} °C</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def dashboard_page():
    """Enhanced dashboard page"""
    st.markdown('<h1 class="main-header">📊 Advanced Battery Dashboard</h1>', unsafe_allow_html=True)
    
    monitor = BatteryMonitor()
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <h2 style="color: #ffa502;">⚠️ No Cells Configured</h2>
            <p style="color: white; font-size: 1.2rem;">Please visit the Setup page to configure your battery cells first.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced control bar
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.markdown(f'<h3 class="neon-text" style="color: #4ECDC4;">🏭 {st.session_state.bench_name} | 👥 Group {st.session_state.group_number}</h3>', 
                   unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Refresh", type="secondary"):
            st.rerun()
    with col3:
        auto_refresh = st.checkbox("⏱️ Auto (10s)", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
    with col4:
        if st.button("🚨 Emergency", help="Emergency stop all cells"):
            for key in st.session_state.cells_data:
                st.session_state.cells_data[key]['current'] = 0.0
            st.error("🛑 All cells stopped!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto refresh logic
    if st.session_state.auto_refresh:
        time.sleep(10)
        st.rerun()
    
    # Enhanced summary metrics
    cells_data = st.session_state.cells_data
    total_cells = len(cells_data)
    charging_cells = sum(1 for data in cells_data.values() if data.get('current', 0) > 0.1)
    discharging_cells = sum(1 for data in cells_data.values() if data.get('current', 0) < -0.1)
    critical_cells = sum(1 for data in cells_data.values() 
                        if data.get('voltage', 0) < data.get('min_voltage', 0) or 
                           data.get('voltage', 0) > data.get('max_voltage', 0) or 
                           data.get('temp', 0) > 50)
    total_power = sum(data.get('voltage', 0) * data.get('current', 0) for data in cells_data.values())
    avg_temp = sum(data.get('temp', 0) for data in cells_data.values()) / len(cells_data)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics = [
        (col1, "🔋", total_cells, "Total Cells", "#4ECDC4"),
        (col2, "🔌", charging_cells, "Charging", "#2ed573"),
        (col3, "⚡", discharging_cells, "Discharging", "#ff416c"),
        (col4, "⚠️", critical_cells, "Critical", "#ff3742"),
        (col5, "💪", f"{total_power:.1f}W", "Total Power", "#ffa502"),
        (col6, "🌡️", f"{avg_temp:.1f}°C", "Avg Temp", "#45b7d1")
    ]
    
    for col, icon, value, label, color in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-container" style="background: linear-gradient(135deg, {color}33, {color}66);">
                <div style="font-size: 2rem;">{icon}</div>
                <h3 style="color: {color};">{value}</h3>
                <p style="margin: 0; color: white;">{label}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced cell grid display
    st.markdown("### 🔋 Live Cell Status Grid")
    cols = st.columns(4)
    
    for idx, (key, data) in enumerate(cells_data.items()):
        col = cols[idx % 4]
        
        current = data.get('current', 0)
        voltage = data.get('voltage', 0)
        temp = data.get('temp', 0)
        min_v = data.get('min_voltage', 0)
        max_v = data.get('max_voltage', 0)
        power = voltage * current
        
        status = monitor.get_cell_status(current, voltage, min_v, max_v, temp)
        status_color = monitor.get_status_color(voltage, min_v, max_v, temp)
        temp_class = monitor.get_temp_class(temp)
        voltage_class = monitor.get_voltage_class(voltage, min_v, max_v)
        power_class = monitor.get_power_class(power)
        
        # Status icons and labels
        status_icons = {
            "charging": "🔋⬆️",
            "discharging": "🔋⬇️", 
            "idle": "🔋⏸️",
            "critical": "🔋⚠️"
        }
        
        status_labels = {
            "charging": "CHARGING",
            "discharging": "DISCHARGING",
            "idle": "STANDBY",
            "critical": "CRITICAL"
        }
        
        with col:
            st.markdown(f"""
            <div class="cell-card {status}">
                <h4 style="color: {data.get('color', '#ffffff')}; margin-bottom: 15px;">
                    {status_icons.get(status, '🔋')} {key.upper()}
                </h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Voltage</div>
                        <div class="{voltage_class}" style="font-size: 1.3rem; font-weight: bold;">
                            ⚡ {voltage:.2f}V
                        </div>
                    </div>
                    
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Current</div>
                        <div style="font-size: 1.3rem; font-weight: bold;">
                            🔌 {current:.2f}A
                        </div>
                    </div>
                    
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Temperature</div>
                        <div class="{temp_class}" style="font-size: 1.3rem; font-weight: bold;">
                            🌡️ {temp:.1f}°C
                        </div>
                    </div>
                    
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Power</div>
                        <div class="{power_class}" style="font-size: 1.3rem; font-weight: bold;">
                            💪 {power:.2f}W
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <div style="font-weight: bold; font-size: 1.1rem;">
                        {status_labels.get(status, 'UNKNOWN')}
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">
                        Charge: {data.get('total_charge', 0):.2f} Ah
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def control_panel_page():
    """Enhanced control panel for charging/discharging"""
    st.markdown('<h1 class="main-header">🎛️ Advanced Control Panel</h1>', unsafe_allow_html=True)
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <h2 style="color: #ffa502;">⚠️ No Cells Configured</h2>
            <p style="color: white; font-size: 1.2rem;">Please visit the Setup page to configure your battery cells first.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced global controls
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🌐 Global Cell Controls")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔋 Charge All", type="primary", use_container_width=True):
            for key in st.session_state.cells_data:
                st.session_state.cells_data[key]['current'] = random.uniform(1.0, 3.0)
            st.success("🔋 All cells charging!")
            
    with col2:
        if st.button("⚡ Discharge All", use_container_width=True):
            for key in st.session_state.cells_data:
                st.session_state.cells_data[key]['current'] = random.uniform(-3.0, -1.0)
            st.success("⚡ All cells discharging!")
    
    with col3:
        if st.button("⏸️ Pause All", use_container_width=True):
            for key in st.session_state.cells_data:
                st.session_state.cells_data[key]['current'] = 0.0
            st.info("⏸️ All cells paused!")
    
    with col4:
        if st.button("🚨 EMERGENCY STOP", help="Immediate stop all operations"):
            for key in st.session_state.cells_data:
                st.session_state.cells_data[key]['current'] = 0.0
                st.session_state.cells_data[key]['voltage'] = st.session_state.cells_data[key].get('min_voltage', 3.0) + 0.2
            st.error("🛑 EMERGENCY STOP ACTIVATED!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced individual cell controls
    st.markdown("### 🔧 Individual Cell Controls")
    
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["🎛️ Quick Controls", "⚙️ Advanced Settings"])
    
    with tab1:
        cols = st.columns(2)
        for idx, (key, data) in enumerate(st.session_state.cells_data.items()):
            col = cols[idx % 2]
            
            with col:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid {data.get('color', '#667eea')};">
                    <h4 style="color: {data.get('color', '#667eea')};">🔋 {key.upper()}</h4>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"🔋 Charge", key=f"charge_{key}", use_container_width=True):
                        st.session_state.cells_data[key]['current'] = random.uniform(1.0, 3.0)
                        st.success(f"🔋 {key} charging!")
                
                with col2:
                    if st.button(f"⚡ Discharge", key=f"discharge_{key}", use_container_width=True):
                        st.session_state.cells_data[key]['current'] = random.uniform(-3.0, -1.0)
                    
