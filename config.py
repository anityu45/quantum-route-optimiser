# config.py
PAGE_CONFIG = {
    "page_title": "Quantum Logistics Pro",
    "page_icon": "⚛️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Cyberpunk / Professional Logistics Theme
CUSTOM_CSS = """
<style>
    .stApp { background-color: #0b1426; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #060a12; }
    h1, h2, h3 { color: #ffffff !important; }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        color: #00e5ff !important;
        font-size: 26px;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
    }
    div[data-testid="stMetricLabel"] { color: #b0bec5 !important; }

    /* Button Styling */
    div.stButton > button:first-child {
        background-color: #2962ff; 
        color: white; border: none; padding: 10px 20px;
        font-weight: bold; border-radius: 8px;
    }
    div.stButton > button:hover { background-color: #0039cb; }
</style>
"""
