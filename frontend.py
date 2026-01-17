# frontend.py
import streamlit as st
import pandas as pd
import folium
from folium import Element
from streamlit_folium import st_folium
from streamlit_searchbox import st_searchbox
from api import search_places

def render_sidebar():
    """Renders the Input Sidebar."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/delivery--v1.png", width=60)
        st.title("Route Settings")
        
        tab_search, tab_upload = st.tabs(["📍 Search", "📂 Upload"])
        
        # --- Search Tab ---
        with tab_search:
            start_loc = st_searchbox(search_places, key="start_box", label="Start Location (Origin)")
            st.markdown("---")
            new_stop = st_searchbox(search_places, key="stop_box", label="Add Stop / Destination")
            
            if st.button("Add Location", use_container_width=True):
                if new_stop:
                    names = [s['name'] for s in st.session_state.stops_data]
                    if new_stop['name'] not in names:
                        st.session_state.stops_data.append(new_stop)
                        st.success("Added!")
                    else:
                        st.warning("Already added.")

        # --- Upload Tab ---
        with tab_upload:
            uploaded = st.file_uploader("Upload CSV", type=['csv'])
            if uploaded and st.button("Process CSV"):
                try:
                    df = pd.read_csv(uploaded)
                    if {'name', 'lat', 'lon'}.issubset(df.columns):
                        for _, row in df.iterrows():
                            st.session_state.stops_data.append({
                                "name": str(row['name']),
                                "coords": (float(row['lat']), float(row['lon']))
                            })
                        st.success(f"Loaded {len(df)} locations!")
                except Exception:
                    st.error("CSV columns needed: name, lat, lon")

        st.divider()
        
        # --- Stop List ---
        if st.session_state.stops_data:
            st.markdown(f"**Stops ({len(st.session_state.stops_data)})**")
            for i, s in enumerate(st.session_state.stops_data):
                c1, c2 = st.columns([0.85, 0.15])
                c1.text(f"{i+1}. {s['name'].split(',')[0]}")
                if c2.button("🗑️", key=f"d{i}"):
                    st.session_state.stops_data.pop(i)
                    st.rerun()
            if st.button("Clear All"):
                st.session_state.stops_data = []
                st.rerun()

        st.divider()
        
        # --- Settings ---
        with st.expander("Logistics Costs"):
            is_round_trip = st.toggle("Return to Start?", value=False)
            col1, col2 = st.columns(2)
            mileage = col1.number_input("Km/L", value=12.0)
            fuel_price = col2.number_input("Fuel ₹", value=96.0)

        go_btn = st.button("RUN QUANTUM ROUTER", type="primary", use_container_width=True)
        return start_loc, is_round_trip, mileage, fuel_price, go_btn

def render_dashboard():
    """Renders the Map and Metrics."""
    if st.session_state.optimized_route:
        m = st.session_state.route_metrics
        d = st.session_state.optimized_route
        
        trip_type = "(Round Trip)" if st.session_state.is_round_trip_active else "(One-Way)"
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Dist. {trip_type}", f"{m['dist']:.1f} km")
        c2.metric("Time", f"{int(m['time']//60)}h {int(m['time']%60)}m")
        c3.metric("Fuel", f"{m['fuel']:.1f} L")
        c4.metric("Cost", f"₹ {m['cost']:,.0f}")

        st.markdown("---")
        st.subheader("Tracking Map")
        map_obj = folium.Map(location=d['coords'][0], zoom_start=11, tiles="Cartodb Dark_Matter")
        
        # 1. Draw Main Route (Blue Solid)
        folium.PolyLine(
            d['geo'], 
            color="#00e5ff", 
            weight=4, 
            opacity=0.8,
            tooltip="Main Route"
        ).add_to(map_obj)
        
        # 2. Draw Return Leg (Red Dotted)
        if 'return_geo' in d and d['return_geo']:
            folium.PolyLine(
                d['return_geo'], 
                color="#ff2b2b", 
                weight=4, 
                opacity=0.8,
                dash_array='10, 10',  
                tooltip="Return to Base"
            ).add_to(map_obj)
        
        # 3. Add Custom CSS Legend to Top-Right
        legend_html = '''
            <div style="
                position: fixed; 
                top: 50px; right: 50px; width: 160px; height: 90px; 
                z-index:9999; font-size:14px;
                background-color: rgba(10, 20, 30, 0.85);
                border: 1px solid #00e5ff;
                border-radius: 8px;
                padding: 10px;
                color: white;
                box-shadow: 0 0 15px rgba(0,0,0,0.5);
                backdrop-filter: blur(4px);
                ">
                <b>&nbsp; Route Legend</b><br>
                &nbsp; <i style="background:#00e5ff; width:25px; height:4px; display:inline-block;"></i>&nbsp; Delivery<br>
                &nbsp; <i style="background: repeating-linear-gradient(90deg, #ff2b2b, #ff2b2b 5px, transparent 5px, transparent 10px); width:25px; height:4px; display:inline-block;"></i>&nbsp; Return
            </div>
            '''
        map_obj.get_root().html.add_child(folium.Element(legend_html))

        # 4. Add Markers
        for i, (loc, name) in enumerate(zip(d['coords'], d['names'])):
            if i == 0:
                icon = folium.Icon(color="green", icon="play")
                popup = "START: Warehouse"
            elif i == len(d['names']) - 1:
                if st.session_state.is_round_trip_active:
                    icon = folium.Icon(color="green", icon="home") 
                    popup = "END: Returned to Base"
                else:
                    icon = folium.Icon(color="red", icon="flag")
                    popup = "END: Final Destination"
            else:
                icon = folium.Icon(color="blue", icon="info-sign")
                popup = f"Stop {i}"
            
            if i == len(d['names']) - 1 and st.session_state.is_round_trip_active:
                pass 
            else:
                folium.Marker(loc, tooltip=popup, popup=name, icon=icon).add_to(map_obj)
            
        st_folium(map_obj, width="100%", height=500)
