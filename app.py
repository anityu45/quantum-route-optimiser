# app.py
import requests
import numpy as np
from geopy.distance import geodesic
from sklearn.cluster import KMeans 

def build_dist_matrix(nodes):
   
    n = len(nodes)
    try:
        coords_str = ";".join([f"{node['coords'][1]},{node['coords'][0]}" for node in nodes])
        url = f"http://router.project-osrm.org/table/v1/driving/{coords_str}?annotations=distance"
        response = requests.get(url, timeout=2) 
        if response.status_code == 200:
            data = response.json()
            if "distances" in data:
                
                raw_matrix = data["distances"]
                
                clean_matrix = [[10000000.0 if x is None else x for x in row] for row in raw_matrix]
                print(f" OSRM Matrix used for {n} nodes.")
                return np.array(clean_matrix) / 1000.0
    except Exception:
        print("OSRM failedtimed out. Falling back to Geodesic.")
        pass 

    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = geodesic(nodes[i]['coords'], nodes[j]['coords']).km
    return matrix

def calculate_total_dist(route_indices, matrix):
    
    dist = 0
    for i in range(len(route_indices)-1):
        dist += matrix[route_indices[i]][route_indices[i+1]]
    return dist


def simulated_quantum_annealing(nodes):
    
    dist_matrix = build_dist_matrix(nodes)
    n = len(nodes)
    if n < 3:
        return nodes
    curr_route = list(range(n))
    curr_len = calculate_total_dist(curr_route, dist_matrix)
    best_route = curr_route[:]
    best_len = curr_len
    
    temperature = (curr_len / n * 100) if curr_len > 0 else 100.0
    cooling_rate = 0.9995 
    no_improvement_threshold = 1000 
    steps_without_improvement = 0
    
    for _ in range(5000):
        temperature *= cooling_rate
        idx1, idx2 = np.random.randint(1, n), np.random.randint(1, n)
        new_route = curr_route[:]
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        new_len = calculate_total_dist(new_route, dist_matrix)
        delta_e = curr_len - new_len
        if delta_e > 0 or np.random.rand() < np.exp(delta_e / temperature):
            curr_route = new_route
            curr_len = new_len
            if curr_len < best_len:
                best_len = curr_len
                best_route = curr_route
                steps_without_improvement = 0
        
        steps_without_improvement += 1
        if steps_without_improvement >= no_improvement_threshold:
            break
                
    return [nodes[i] for i in best_route]

def solve_hybrid_quantum(start_node, stops_data):
   
    all_nodes = [start_node] + stops_data
    n = len(all_nodes)
    
    
    if n < 10: 
        return simulated_quantum_annealing(all_nodes)
  
    coords = [[s['coords'][0], s['coords'][1]] for s in stops_data]
    k = max(1, n // 5) # Adaptive cluster size
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(coords)
    
    clusters = {i: [] for i in range(k)}
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(stops_data[idx])
        
    cluster_centroids = {}
    for label, points in clusters.items():
        if not points: continue
        lats = [p['coords'][0] for p in points]
        lons = [p['coords'][1] for p in points]
        cluster_centroids[label] = (sum(lats)/len(lats), sum(lons)/len(lons))

    final_route = [start_node]
    remaining_clusters = list(cluster_centroids.keys())
    
    while remaining_clusters:

        curr_pos = final_route[-1]['coords']
        nearest_cluster_idx = min(remaining_clusters, key=lambda c: geodesic(curr_pos, cluster_centroids[c]).km)
        
        sub_stops = clusters[nearest_cluster_idx]
        optimized_sub = simulated_quantum_annealing([final_route[-1]] + sub_stops)
        final_route.extend(optimized_sub[1:])
        
        remaining_clusters.remove(nearest_cluster_idx)
        
    return final_route