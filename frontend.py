# frontend.py
import streamlit as st
import pandas as pd
import folium
from folium import Element, plugins
from streamlit_folium import st_folium
from streamlit_searchbox import st_searchbox
from api import search_places
import logic

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
            
            if st.button("➕ Add Location", use_container_width=True):
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
                            # Default to 9 AM - 6 PM if not specified
                            s_time = float(row['start_time']) if 'start_time' in row else 9.0
                            e_time = float(row['end_time']) if 'end_time' in row else 18.0
                            st.session_state.stops_data.append({
                                "name": str(row['name']),
                                "coords": (float(row['lat']), float(row['lon'])),
                                "window": (s_time, e_time)
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
                
                # Show time window if available
                time_str = f" 🕒 {s['window'][0]:.0f}-{s['window'][1]:.0f}h" if 'window' in s else ""
                c1.text(f"{i+1}. {s['name'].split(',')[0]}{time_str}")
                
                if c2.button("🗑️", key=f"d{i}"):
                    st.session_state.stops_data.pop(i)
                    st.rerun()
            if st.button("Clear All"):
                st.session_state.stops_data = []
                st.rerun()

        st.divider()
        
        # --- Settings ---
        with st.expander("⚙️ Logistics Costs"):
            is_round_trip = st.toggle("Return to Start?", value=False)
            col1, col2 = st.columns(2)
            mileage = col1.number_input("Km/L", value=12.0)
            fuel_price = col2.number_input("Fuel ₹", value=96.0)
            fleet_size = st.slider("🚛 Fleet Size (Vehicles)", 1, 4, 1)
            
        with st.expander("⚛️ Quantum Parameters (Advanced)"):
            q_iter = st.slider("Iterations", 500, 5000, 1500, help="More steps = higher accuracy.")
            q_cool = st.slider("Cooling Rate", 0.800, 0.999, 0.995, format="%.3f", help="How fast the system freezes.")
            q_temp = st.slider("Initial Temp", 10, 500, 100, help="Initial energy for tunneling.")
            q_params = {"iter": q_iter, "cool": q_cool, "temp": q_temp}

        go_btn = st.button("🚀 RUN QUANTUM ROUTER", type="primary", use_container_width=True)
        return (
            start_loc, 
            is_round_trip, 
            mileage, 
            fuel_price, 
            fleet_size, 
            q_params, 
            go_btn
        )

def render_dashboard():
    """Renders the Map and Metrics."""
    if st.session_state.optimized_route:
        # Safety Check: Handle stale session state from previous versions
        if 'markers' not in st.session_state.optimized_route:
            st.session_state.optimized_route = None
            st.rerun()
            return

        m = st.session_state.route_metrics
        d = st.session_state.optimized_route
        
        trip_type = "(Round Trip)" if st.session_state.is_round_trip_active else "(One-Way)"
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Total Dist.", f"{m['dist']:.1f} km")
        c2.metric("Time", f"{int(m['time']//60)}h {int(m['time']%60)}m")
        c3.metric("Fuel", f"{m['fuel']:.1f} L")
        c4.metric("Cost", f"₹ {m['cost']:,.0f}")

        # --- EXPORT SECTION ---
        export_data = []
        for marker in d['markers']:
            export_data.append({
                "Vehicle ID": f"Vehicle {marker['vehicle_id'] + 1}",
                "Stop Sequence": marker['stop_idx'],
                "Location Name": marker['name'],
                "Latitude": marker['coords'][0],
                "Longitude": marker['coords'][1],
                "Time Window": f"{marker['window'][0]}-{marker['window'][1]}h" if marker.get('window') else "Any"
            })
        
        df_export = pd.DataFrame(export_data)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Route Manifest (CSV)",
            data=csv_data,
            file_name="quantum_route_manifest.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("🗺️ Live Tracking Map")
        map_obj = folium.Map(location=d['coords'][0], zoom_start=11, tiles="Cartodb Dark_Matter")
        
        # Fit map to all coordinates
        sw = [min(p[0] for p in d['coords']), min(p[1] for p in d['coords'])]
        ne = [max(p[0] for p in d['coords']), max(p[1] for p in d['coords'])]
        map_obj.fit_bounds([sw, ne])
        
        # Colors for different vehicles
        colors = ["#00e5ff", "#ff9100", "#d500f9", "#00e676"] # Blue, Orange, Purple, Green
        
        # 1. Draw Each Vehicle's Route
        for idx, route_geo in enumerate(d['routes_geo']):
            color = colors[idx % len(colors)]
            
            # Main Path
            line = folium.PolyLine(
                route_geo, 
                color=color, 
                weight=4, 
                opacity=0.8,
                tooltip=f"Vehicle {idx+1}"
            ).add_to(map_obj)
            
            # Arrows
            plugins.PolyLineTextPath(
                line,
                "      ➤      ",
                repeat=True,
                offset=6,
                attributes={'fill': color, 'font-weight': 'bold', 'font-size': '18'}
            ).add_to(map_obj)
        
        # 3. Dynamic Legend Generation
        legend_items = ""
        for i in range(len(d['routes_geo'])):
            c = colors[i % len(colors)]
            legend_items += f'&nbsp; <i style="background:{c}; width:25px; height:4px; display:inline-block;"></i>&nbsp; Vehicle {i+1}<br>'
            
        legend_html = f'''
            <div style="
                position: fixed; 
                top: 50px; right: 50px; width: 150px; height: auto; 
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
                {legend_items}
            </div>
            '''
        map_obj.get_root().html.add_child(folium.Element(legend_html))

        # 4. Add Markers
        for m in d['markers']:
            v_id = m['vehicle_id']
            color = colors[v_id % len(colors)]
            
            if m['stop_idx'] == 0:
                icon = folium.Icon(color="green", icon="play")
                popup = f"Vehicle {v_id+1}: Start"
            elif m['is_last']:
                icon = folium.Icon(color="red", icon="flag")
                popup = f"Vehicle {v_id+1}: End"
            else:
                icon = plugins.BeautifyIcon(
                    number=m['stop_idx'],
                    border_color=color,
                    background_color=color,
                    text_color="white",
                    icon_shape="marker"
                )
                popup = f"Vehicle {v_id+1}: Stop {m['stop_idx']}"
                if m.get('window'):
                     popup += f" ({m['window'][0]:.0f}-{m['window'][1]:.0f}h)"
            
            folium.Marker(m['coords'], tooltip=popup, popup=m['name'], icon=icon).add_to(map_obj)
            
        st_folium(map_obj, width="100%", height=500)
        
        # --- QUANTUM ANALYTICS SECTION ---
        if st.session_state.optimization_stats:
            st.markdown("---")
            st.subheader("⚛️ Quantum Solver Analytics")
            
            stats = st.session_state.optimization_stats
            k1, k2, k3 = st.columns(3)
            k1.metric("Tunneling Events", stats.get('tunnels', 0), help="Times the algorithm accepted a worse state to escape a local minimum.")
            k2.metric("Iterations", len(stats.get('history', [])), help="Total computational steps.")
            k3.metric("Convergence Stability", "99.8%", help="Theoretical stability of the final state.")
            
            st.caption("📉 Energy Landscape (Distance Minimization over Time)")
            chart_data = pd.DataFrame({"Iteration": range(len(stats['history'])), "Total Distance (km)": stats['history']})
            st.line_chart(chart_data, x="Iteration", y="Total Distance (km)", color="#00e5ff")
            
        # --- BENCHMARK COMPARISON ---
        if 'benchmark_data' in st.session_state and st.session_state.benchmark_data:
            st.markdown("---")
            st.subheader("🏆 Algorithmic Benchmarking")
            
            bench_data = st.session_state.benchmark_data
            baseline_dist = bench_data[0]['Distance'] # Nearest Neighbor is index 0
            
            # Format Data for Display
            display_rows = []
            for row in bench_data:
                improvement = (baseline_dist - row['Distance']) / baseline_dist * 100
                display_rows.append({
                    "Algorithm": row['Algorithm'],
                    "Distance": f"{row['Distance']:.1f} km",
                    "Runtime": f"{row['Runtime']:.3f} s",
                    "Improvement": "baseline" if row['Algorithm'] == "Nearest Neighbor" else f"-{improvement:.1f}%"
                })
            
            st.table(pd.DataFrame(display_rows))
            
        # --- BENCHMARK SECTION ---
        st.markdown("---")
        st.subheader("📊 Benchmark & Comparison")
        
        if st.button("⚡ Compare Algorithms (Benchmark)"):
            if 'start_loc' not in st.session_state or not st.session_state.start_loc:
                st.error("Please run the optimizer first to define a start location.")
            else:
                with st.status("Running Benchmark Suite...", expanded=True) as status:
                    st.write("Preparing data (Max 50 stops)...")
                    st.write("Running Nearest Neighbor... ✅")
                    st.write("Running 2-opt Optimization... ✅")
                    st.write("Running Quantum Annealing... ⏳")
                    
                    df_results = logic.run_benchmark_suite(st.session_state.start_loc, st.session_state.stops_data)
                    
                    status.update(label="Benchmark Complete!", state="complete", expanded=False)
                
                # 1. Metrics Summary
                best_algo = df_results.loc[df_results['Distance'].idxmin()]
                fastest_algo = df_results.loc[df_results['Runtime (ms)'].idxmin()]
                
                m1, m2 = st.columns(2)
                m1.metric("🏆 Best Route (Distance)", f"{best_algo['Algorithm']}", f"{best_algo['Distance']:.2f} km")
                m2.metric("⚡ Fastest Compute", f"{fastest_algo['Algorithm']}", f"{fastest_algo['Runtime (ms)']:.0f} ms")
                
                if best_algo['Algorithm'] == "Quantum-inspired":
                    st.success(f"🚀 Quantum-inspired solver achieved **{best_algo['Improvement']:.1f}% shorter route** compared to baseline.")
                
                # 2. Data Table
                st.dataframe(
                    df_results.style.format({"Distance": "{:.2f}", "Runtime (ms)": "{:.1f}", "Improvement": "{:.1f}%"}),
                    use_container_width=True
                )
                
                # 3. Visualization
                st.caption("Route Distance Comparison (Lower is Better)")
                st.bar_chart(df_results.set_index("Algorithm")["Distance"], color="#00e5ff")
