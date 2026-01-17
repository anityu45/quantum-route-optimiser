import streamlit as st

def init_session():
    # Store the list of stops
    if 'stops' not in st.session_state:
        st.session_state.stops = []
    
    # Store the calculated route
    if 'route_data' not in st.session_state:
        st.session_state.route_data = None
        
    # Store metrics (distance, time)
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {"dist": 0, "time": 0}

def clear_data():
    st.session_state.stops = []
    st.session_state.route_data = None
    st.session_state.metrics = {"dist": 0, "time": 0}