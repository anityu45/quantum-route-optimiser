# logic.py
import time
import pandas as pd
import streamlit as st
import app as quantum_solver

def optimize_route_algo(start, stops, round_trip=False, fleet_size=1, quantum_params=None):
    """
    Router Logic.
    Strictly calls the Hybrid Quantum Solver.
    NO Classical OR-Tools allowed.
    """
    # 1. Execute Quantum-Inspired Optimization
    # Returns a LIST of routes (even if just 1)
    routes, stats = quantum_solver.solve_hybrid_quantum(start, stops, n_vehicles=fleet_size, q_params=quantum_params)
    
    # 2. Handle Round Trip (Return to Warehouse)
    # If fleet > 1, round trip is mandatory (Hub -> Nodes -> Hub)
    if round_trip or fleet_size > 1:
        for i in range(len(routes)):
            # Append start node to end of each route
            routes[i].append(routes[i][0])
        
    return routes, stats

@st.cache_data(show_spinner=False)
def run_benchmark_suite(start_node, stops_data):
    """
    Runs NN, 2-opt, and Quantum algorithms to compare performance.
    Cached based on input data to avoid re-running on every refresh.
    """
    # Limit to 50 stops for benchmark speed
    bench_stops = stops_data[:50]
    all_nodes = [start_node] + bench_stops
    n = len(all_nodes)
    
    # Build matrices once
    dist_matrix, time_matrix = quantum_solver.build_matrices(all_nodes)
    
    results = []
    
    # 1. Nearest Neighbor
    t0 = time.time()
    nn_route = quantum_solver.solve_nearest_neighbor(n, dist_matrix)
    nn_dist = quantum_solver.calculate_route_distance(nn_route, dist_matrix)
    t1 = time.time()
    results.append({
        "Algorithm": "Nearest Neighbor", 
        "Distance": nn_dist, 
        "Runtime (ms)": (t1 - t0) * 1000,
        "Improvement": 0.0
    })
    
    # 2. 2-opt Improved
    t0 = time.time()
    to_route = quantum_solver.solve_two_opt(all_nodes, dist_matrix, time_matrix)
    to_dist = quantum_solver.calculate_route_distance(to_route, dist_matrix)
    t1 = time.time()
    imp_to = ((nn_dist - to_dist) / nn_dist) * 100
    results.append({
        "Algorithm": "2-opt Improved", 
        "Distance": to_dist, 
        "Runtime (ms)": (t1 - t0) * 1000,
        "Improvement": imp_to
    })
    
    # 3. Quantum-inspired (Fast Mode)
    t0 = time.time()
    # Use reduced iterations for speed in benchmark
    fast_params = {"iter": 600, "cool": 0.90, "temp": 100}
    q_routes, _ = quantum_solver.solve_hybrid_quantum(start_node, bench_stops, n_vehicles=1, q_params=fast_params)
    
    # Map nodes back to indices to calculate pure distance
    q_nodes = q_routes[0]
    q_indices = [all_nodes.index(node) for node in q_nodes if node in all_nodes]
    q_dist = quantum_solver.calculate_route_distance(q_indices, dist_matrix)
    t1 = time.time()
    
    imp_q = ((nn_dist - q_dist) / nn_dist) * 100
    results.append({
        "Algorithm": "Quantum-inspired", 
        "Distance": q_dist, 
        "Runtime (ms)": (t1 - t0) * 1000,
        "Improvement": imp_q
    })
    
    return pd.DataFrame(results)
