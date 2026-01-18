# main.py
import streamlit as st
import config
import sessionstate
import logic
import api
import frontend

# 1. Setup Page & State
st.set_page_config(**config.PAGE_CONFIG)
st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)
sessionstate.init_session_state()

st.title("⚛️ Quantum Logistics Pro")
if not st.session_state.optimized_route:
    st.info("👈 Please configure your stops in the sidebar and click RUN to start.")

# 2. Render Sidebar Inputs
start_loc, is_round_trip, mileage, fuel_price, fleet_size, q_params, go_btn = frontend.render_sidebar()

# Store start_loc for benchmarking access later
if start_loc: st.session_state.start_loc = start_loc

# 3. Main Application Logic
if go_btn:
    if not start_loc:
        st.error("⚠️ Please select a Start Location.")
    elif not st.session_state.stops_data:
        st.error("⚠️ Please add at least one stop.")
    else:
        with st.spinner("⚛️ Initializing Quantum Tunneling Simulation..."):
            
            st.session_state.is_round_trip_active = is_round_trip
            
            # --- CALL QUANTUM SOLVER ---
            # Logic returns the full ordered list. 
            # If round_trip=True, the last node in sorted_nodes is the Start Node.
            routes_list, stats = logic.optimize_route_algo(
                start_loc, 
                st.session_state.stops_data, 
                round_trip=is_round_trip,
                fleet_size=fleet_size,
                quantum_params=q_params
            )
            
            # --- SPLIT PATH PROCESSING ---
            total_km = 0
            total_min = 0
            all_routes_geo = []
            all_markers = []
            all_coords = []
            
            for v_idx, route_nodes in enumerate(routes_list):
                # Get Geometry for this specific vehicle route
                coords_seq = [n['coords'] for n in route_nodes]
                path_geo, km, mins = api.get_road_path(coords_seq)
                
                total_km += km
                total_min += mins
                all_routes_geo.append(path_geo if path_geo else coords_seq)
                
                # Collect Marker Data with Vehicle Info
                for s_idx, node in enumerate(route_nodes):
                    all_markers.append({
                        "coords": node['coords'],
                        "name": node['name'],
                        "vehicle_id": v_idx,
                        "stop_idx": s_idx,
                        "is_last": s_idx == len(route_nodes) - 1,
                        "window": node.get('window')
                    })
                    all_coords.append(node['coords'])
            
            # --- CALCULATE LOGISTICS METRICS ---
            total_fuel = total_km / mileage
            total_cost = total_fuel * fuel_price
            
            # --- UPDATE SESSION STATE ---
            st.session_state.route_metrics = {
                "dist": total_km,
                "time": total_min,
                "fuel": total_fuel,
                "cost": total_cost
            }
            
            # Store split geometries so Frontend can color them differently
            st.session_state.optimized_route = {
                "markers": all_markers,
                "coords": all_coords,
                "routes_geo": all_routes_geo # List of geometries
            }
            
            # Store Quantum Analytics
            st.session_state.optimization_stats = stats
            
            st.rerun()

# 4. Render Results Dashboard
frontend.render_dashboard()
