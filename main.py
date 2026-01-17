import streamlit as st
import config, sessionstate, frontend, logic, api

st.set_page_config(page_title="Quantum Logistics", layout="wide")
config.load_css()
sessionstate.init_session_state()

st.title("Quantum Logistics Optimizer")


start_loc, is_round_trip, mileage, fuel_price, go_btn = frontend.render_sidebar()


if go_btn:
    if not start_loc:
        st.error("Please select a start location.")
    elif not st.session_state.stops_data:
        st.error("Please add at least one stop.")
    else:
        with st.spinner("Calculating Quantum Route..."):
           
            st.session_state.is_round_trip_active = is_round_trip
            
           
            ordered_nodes = logic.optimize_route_algo(start_loc, st.session_state.stops_data, is_round_trip)

            main_nodes = ordered_nodes
            return_nodes = []
            
            if is_round_trip and len(ordered_nodes) > 1:
                main_nodes = ordered_nodes[:-1]
                return_nodes = [ordered_nodes[-2], ordered_nodes[-1]]
            
            
            main_geo, m_dist, m_time = api.get_road_path([n['coords'] for n in main_nodes])
            
            ret_geo, r_dist, r_time = [], 0, 0
            if return_nodes:
                ret_geo, r_dist, r_time = api.get_road_path([n['coords'] for n in return_nodes])
            
        
            st.session_state.optimized_route = {
                "coords": [n['coords'] for n in ordered_nodes],
                "names": [n['name'] for n in ordered_nodes],
                "geo": main_geo if main_geo else [],
                "return_geo": ret_geo if ret_geo else []
            }
            
            total_dist = m_dist + r_dist
            fuel = total_dist / mileage if mileage else 0
            st.session_state.route_metrics = {
                "dist": total_dist,
                "time": m_time + r_time,
                "fuel": fuel,
                "cost": fuel * fuel_price
            }
            st.rerun()


frontend.render_dashboard()
