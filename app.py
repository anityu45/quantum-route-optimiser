# app.py
import requests
import numpy as np
from geopy.distance import geodesic
from sklearn.cluster import KMeans 

# ======================================================
# 1. GEOMETRY & DATA FETCHING
# ======================================================

def build_matrices(nodes):
    """
    Creates Distance AND Time matrices.
    Returns: (dist_matrix_km, time_matrix_hours)
    """
    n = len(nodes)
    
    # 1. Try OSRM Table API (Real Road Distance)
    try:
        # OSRM requires Lon,Lat format
        coords_str = ";".join([f"{node['coords'][1]},{node['coords'][0]}" for node in nodes])
        url = f"http://router.project-osrm.org/table/v1/driving/{coords_str}?annotations=distance,duration"
        
        response = requests.get(url, timeout=3) 
        if response.status_code == 200:
            data = response.json()
            if "distances" in data and "durations" in data:
                raw_dist = data["distances"]
                raw_time = data["durations"]
                
                # Handle None (unreachable) as a very high penalty distance
                clean_dist = [[99999.0 if x is None else x for x in row] for row in raw_dist]
                clean_time = [[99999.0 if x is None else x for x in row] for row in raw_time]
                
                print(f"✅ OSRM Matrices generated for {n} nodes.")
                # Return km and hours
                return np.array(clean_dist) / 1000.0, np.array(clean_time) / 3600.0
    except Exception as e:
        print(f"⚠️ OSRM Matrix failed: {e}. Falling back to Geodesic.")

    # 2. Fallback: Geodesic (As the Crow Flies)
    dist_matrix = np.zeros((n, n))
    time_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                d = geodesic(nodes[i]['coords'], nodes[j]['coords']).km
                dist_matrix[i][j] = d
                time_matrix[i][j] = d / 50.0 # Assume 50km/h avg speed
                
    return dist_matrix, time_matrix

def calculate_energy(route_indices, dist_matrix, time_matrix, nodes):
    """
    Calculates Total Energy = Distance + (Penalty * Lateness).
    """
    total_dist = 0
    current_time = 8.0 # Start day at 8 AM
    
    for i in range(len(route_indices)-1):
        u, v = route_indices[i], route_indices[i+1]
        total_dist += dist_matrix[u][v]
        current_time += time_matrix[u][v]
        
        # Check Time Window for destination 'v'
        if 'window' in nodes[v]:
            start_w, end_w = nodes[v]['window']
            # If early, we wait (no penalty, but time advances)
            if current_time < start_w:
                current_time = start_w
            # If late, massive penalty (1 hour late = 100km penalty)
            elif current_time > end_w:
                overdue = current_time - end_w
                total_dist += (overdue * 100.0) 
                
    return total_dist

# ======================================================
# 2. QUANTUM-INSPIRED SOLVER (Simulated Annealing)
# ======================================================

def simulated_quantum_annealing(nodes, q_params=None):
    """
    THE QUANTUM SIMULATION (Metropolis-Hastings Algorithm).
    Simulates thermal fluctuations to tunnel through energy barriers (local minima).
    """
    dist_matrix, time_matrix = build_matrices(nodes)
    n = len(nodes)
    
    if n < 3:
        return nodes, {"history": [], "tunnels": 0, "final_temp": 0}
         
    # Default Physics
    if q_params is None: q_params = {}
    p_iter = q_params.get("iter", 3000)
    p_cool = q_params.get("cool", 0.998)
    p_temp = q_params.get("temp", 100)
    
    # Initial State
    # IMPROVEMENT 1: Greedy Initialization (Nearest Neighbor)
    # Starts the annealing process from a decent solution instead of a random one.
    unvisited = set(range(1, n))
    curr_route = [0]
    curr_node = 0
    while unvisited:
        next_node = min(unvisited, key=lambda x: dist_matrix[curr_node][x])
        curr_route.append(next_node)
        unvisited.remove(next_node)
        curr_node = next_node
        
    curr_len = calculate_energy(curr_route, dist_matrix, time_matrix, nodes)
    best_route = curr_route[:]
    best_len = curr_len
    
    # Analytics Tracking
    energy_history = []
    tunneling_events = 0
    
    # Physics Parameters
    # Starting temperature scaled by route length to handle different map scales
    temperature = (curr_len / n) * p_temp 
    cooling_rate = p_cool
    
    # Dynamic iterations based on user input
    for _ in range(p_iter):
        temperature *= cooling_rate
        
        new_route = curr_route[:]
        
        # IMPROVEMENT 2: Hybrid Mutation (Swap + 2-Opt)
        # 50% chance to Swap (Teleport), 50% chance to Reverse (Untangle)
        if np.random.rand() < 0.5:
            idx1, idx2 = np.random.randint(1, n), np.random.randint(1, n)
            new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        else:
            # 2-Opt: Reverse a segment to untangle crossing paths
            i, j = np.random.randint(1, n), np.random.randint(1, n)
            if i > j: i, j = j, i
            # Reverse the sub-segment
            new_route[i:j+1] = new_route[i:j+1][::-1]
        
        new_len = calculate_energy(new_route, dist_matrix, time_matrix, nodes)
        
        # Acceptance Criterion (Metropolis Logic)
        # P = exp(-dE / T)
        if new_len < curr_len or np.random.rand() < np.exp((curr_len - new_len) / temperature):
            if new_len > curr_len:
                tunneling_events += 1
            curr_route = new_route
            curr_len = new_len
            if curr_len < best_len:
                best_len = curr_len
                best_route = curr_route
        
        energy_history.append(curr_len)

    # IMPROVEMENT 3: Deterministic 2-Opt Polish
    # Annealing finds the "valley", 2-Opt finds the very bottom.
    # We run a quick pass to untangle any remaining knots.
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_route = best_route[:]
                new_route[i:j+1] = best_route[i:j+1][::-1]
                new_len = calculate_energy(new_route, dist_matrix, time_matrix, nodes)
                
                if new_len < best_len:
                    best_route = new_route
                    best_len = new_len
                    improved = True
                
    return [nodes[i] for i in best_route], {
        "history": energy_history,
        "tunnels": tunneling_events,
        "final_temp": temperature
    }

# ======================================================
# 3. HYBRID DISPATCHER (Clustering + Nearest-Neighbor)
# ======================================================

def solve_hybrid_quantum(start_node, stops_data, n_vehicles=1, q_params=None):
    """
    Hybrid Solver.
    Combines K-Means clustering with Quantum-Inspired sequencing.
    Returns: List of Routes (each route is a list of nodes), Stats
    """
    all_nodes = [start_node] + stops_data
    n = len(all_nodes)
    
    # If 1 vehicle and small dataset, simple anneal
    if n_vehicles == 1 and n < 25: 
        r, s = simulated_quantum_annealing(all_nodes, q_params)
        return [r], s
    
    # --- STEP 1: Clustering (Classical ML) ---
    coords = [[s['coords'][0], s['coords'][1]] for s in stops_data]
    
    # If Multi-Vehicle, k = fleet_size. Else dynamic k.
    k = n_vehicles if n_vehicles > 1 else max(1, n // 5)
    
    # Handle edge case where stops < vehicles
    if len(stops_data) < k:
        k = len(stops_data)
        
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(coords)
    
    clusters = {i: [] for i in range(k)}
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(stops_data[idx])
        
    combined_stats = {"history": [], "tunnels": 0, "final_temp": 0}

    # --- CASE A: MULTI-VEHICLE (Independent Loops) ---
    if n_vehicles > 1:
        routes = []
        for label, sub_stops in clusters.items():
            if not sub_stops: continue
            # Each vehicle starts at Hub, visits cluster, returns to Hub (handled in main or here)
            # We just optimize [Hub] + [Cluster Nodes]
            
            # Recursively use single-vehicle logic to optimize this specific cluster
            # This ensures large clusters are further broken down if necessary
            sub_routes, stats = solve_hybrid_quantum(start_node, sub_stops, n_vehicles=1, q_params=q_params)
            routes.append(sub_routes[0])
            combined_stats["tunnels"] += stats["tunnels"]
            combined_stats["history"].extend(stats["history"])
        return routes, combined_stats

    # --- STEP 2: Intelligent Cluster Dispatching ---
    # We navigate from cluster to cluster based on proximity
    final_route = [start_node]
    remaining_clusters = [k for k in clusters.keys() if clusters[k]]
    

    while remaining_clusters:
        # Find the geographically nearest cluster to our current location
        curr_pos = final_route[-1]['coords']
        
        # IMPROVEMENT 4: Single Linkage Clustering
        # Instead of centroids, find the cluster containing the closest individual node.
        def get_min_dist_to_cluster(c_idx):
            return min(geodesic(curr_pos, node['coords']).km for node in clusters[c_idx])

        nearest_cluster_idx = min(remaining_clusters, key=get_min_dist_to_cluster)
        
        sub_stops = clusters[nearest_cluster_idx]
        
        # Optimize the sequence within this cluster
        # We pass the last node of our current route as the 'start' for the next cluster
        optimized_sub, stats = simulated_quantum_annealing([final_route[-1]] + sub_stops, q_params)
        
        # Add optimized cluster points to final route (skipping index 0 which is final_route[-1])
        final_route.extend(optimized_sub[1:])
        
        # Aggregate Stats
        combined_stats["history"].extend(stats["history"])
        combined_stats["tunnels"] += stats["tunnels"]
        remaining_clusters.remove(nearest_cluster_idx)
        
    return [final_route], combined_stats