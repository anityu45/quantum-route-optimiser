# sessionstate.py
import streamlit as st
import uuid

def init_session_state():
    """Initialize all session variables if they don't exist."""
    if 'stops_data' not in st.session_state:
        st.session_state.stops_data = [] 
        
    if 'optimized_route' not in st.session_state:
        st.session_state.optimized_route = None
        
    if 'route_metrics' not in st.session_state:
        st.session_state.route_metrics = {}
        
    if 'user_agent_id' not in st.session_state:
        st.session_state.user_agent_id = str(uuid.uuid4())
        
    if 'is_round_trip_active' not in st.session_state:
        st.session_state.is_round_trip_active = False
        
    if 'optimization_stats' not in st.session_state:
        st.session_state.optimization_stats = None
        
    if 'solver_status' not in st.session_state:
        st.session_state.solver_status = "Idle"
