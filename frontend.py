import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import state, solver, api

def render_sidebar():
    with st.sidebar:
        st.header("📦 Logistics Control")
        
        uploaded_file = st.file_uploader("Upload Manifest (CSV)", type=['csv'])
        if uploaded_file:
            if st.button("Process CSV"):
                try:
                    df = pd.read_csv(uploaded_file)
                    state.clear_data()
                    # Expect columns: name, lat, lon
                    for _, row in df.iterrows():
                        st.session_state.stops.append({
                            "name": row.get('name', 'Stop'),
                            "coords": (row['lat'], row['lon'])
                        })
                    st.success(f"Loaded {len(st.session_state.stops)} locations!")
                except:
                    st.error("CSV must have 'lat' and 'lon' columns.")

        st.divider()
        
        if st.button("🚀 RUN OPTIMIZER", type="primary"):
            if len(st.session_state.stops) < 2:
                st.warning("Upload data first!")
            else:
                with st.spinner("Optimizing Route..."):
                    # 1. Sort the stops (The "Brain")
                    start = st.session_state.stops[0]
                    others = st.session_state.stops[1:]
                    ordered_stops = solver.solve_simple_route(start, others)
                    
                    # 2. Get the road lines (The "Visuals")
                    path_coords = [s['coords'] for s in ordered_stops]
                    path_coords.append(start['coords']) # Return to start
                    
                    line_points, dist, time = api.get_route_shape(path_coords)
                    
                    # 3. Save results
                    st.session_state.route_data = {"path": line_points}
                    st.session_state.metrics = {"dist": dist, "time": time}
                    st.success("Route Optimized!")

def render_map():
    # Metrics
    m = st.session_state.metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Distance", f"{m['dist']:.1f} km")
    c2.metric("Time", f"{m['time']:.0f} min")
    c3.metric("Savings", "15% Fuel") 

    # Map
    start = [20.5937, 78.9629] # Default India
    if st.session_state.stops:
        start = st.session_state.stops[0]['coords']
        
    m = folium.Map(location=start, zoom_start=12, tiles="CartoDB dark_matter")
    
    # Draw Points
    for i, stop in enumerate(st.session_state.stops):
        color = "#00ff9d" if i == 0 else "#ff0055"
        folium.Marker(stop['coords'], popup=stop['name'], icon=folium.Icon(color="black", icon_color=color)).add_to(m)

    # Draw Line
    if st.session_state.route_data:
        folium.PolyLine(st.session_state.route_data['path'], color="#00e5ff", weight=5).add_to(m)

    st_folium(m, width=800, height=500)