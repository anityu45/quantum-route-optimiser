# config.py
import streamlit as st

PAGE_CONFIG = {
    "page_title": "Quantum Logistics Pro",
    "page_icon": "⚛️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Cyberpunk / Professional Logistics Theme
CUSTOM_CSS = """
<style>
    /* Import Fonts: Orbitron (Futuristic) & Roboto (Clean) */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Roboto:wght@300;400;700&display=swap');

    /* Global App Background */
    .stApp {
        background: radial-gradient(circle at top left, #0b1021 0%, #05050a 100%);
        color: #e0e6ed;
        font-family: 'Roboto', sans-serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 12, 20, 0.95);
        border-right: 1px solid rgba(0, 243, 255, 0.1);
    }
    
    /* Headings (Neon Gradients) */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        background: -webkit-linear-gradient(0deg, #00f3ff, #bc13fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }
    
    /* Glassmorphism Cards (Metrics, Expanders, Containers) */
    div[data-testid="stMetric"], div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 243, 255, 0.4);
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
    }

    /* Metric Values (Neon Cyan) */
    div[data-testid="stMetricValue"] {
        color: #00f3ff !important;
        font-family: 'Orbitron', sans-serif;
        font-size: 28px !important;
        text-shadow: 0 0 12px rgba(0, 243, 255, 0.6);
    }
    div[data-testid="stMetricLabel"] {
        color: #a0aab5 !important;
        font-size: 14px !important;
        font-weight: 400;
    }

    /* Buttons (Neon Borders & Glow) */
    div.stButton > button {
        background: transparent !important;
        border: 1px solid #00f3ff !important;
        color: #00f3ff !important;
        border-radius: 12px !important;
        font-family: 'Orbitron', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: rgba(0, 243, 255, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Cyberpunk Launch Button */
    div.stButton > button[kind="primary"] {
        background: transparent !important;
        border: 2px solid #00f3ff !important;
        color: #00f3ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 10px rgba(0, 243, 255, 0.1);
    }
    
    div.stButton > button[kind="primary"]:hover {
        background: rgba(0, 243, 255, 0.1) !important;
        box-shadow: 0 0 30px rgba(0, 243, 255, 0.6), inset 0 0 20px rgba(0, 243, 255, 0.4);
        text-shadow: 0 0 8px rgba(0, 243, 255, 0.8);
        transform: translateY(-2px);
    }

    /* Scanline Animation */
    div.stButton > button[kind="primary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.5), transparent);
        animation: scanline 3s infinite linear;
    }

    @keyframes scanline {
        0% { left: -100%; }
        20% { left: 100%; }
        100% { left: 100%; }
    }

    /* Download Button Styling (Consistent with Theme) */
    div[data-testid="stDownloadButton"] > button {
        background: rgba(188, 19, 254, 0.1) !important;
        border: 1px solid #bc13fe !important;
        color: #bc13fe !important;
        font-family: 'Orbitron', sans-serif !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        box-shadow: 0 0 15px rgba(188, 19, 254, 0.4);
        transform: translateY(-2px);
        color: #fff !important;
    }

    /* Table/Dataframe Styling */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
</style>
"""

def load_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
