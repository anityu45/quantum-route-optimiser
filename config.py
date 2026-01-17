import streamlit as st

def load_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0b1426; color: #e0e0e0; }
        [data-testid="stSidebar"] { background-color: #060a12; border-right: 1px solid #1e2a45; }
        .stButton>button { color: #00e5ff; border: 1px solid #00e5ff; background-color: transparent; }
        .stButton>button:hover { background-color: #00e5ff; color: #000; }
        h1, h2, h3 { color: #00e5ff !important; font-family: 'Courier New', monospace; }
        .stSuccess { background-color: #1e3a2f; color: #00ff9d; }
        </style>
    """, unsafe_allow_html=True)