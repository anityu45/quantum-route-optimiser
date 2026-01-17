# app.py
import numpy as np
from geopy.distance import geodesic
from sklearn.cluster import KMeans 


def build_dist_matrix(nodes):

    n = len(nodes)
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
    if n < 2: return nodes
    
    
    curr_route = list(range(n))
    curr_len = calculate_total_dist(curr_route, dist_matrix)
    best_route = curr_route[:]
    best_len = curr_len
    
  
    temperature = 1000  
    cooling_rate = 0.995 
    
    # The Annealing Process
    for _ in range(500):
        temperature *= cooling_rate
        
        idx1, idx2 = np.random.randint(1, n), np.random.randint(1, n)
        new_route = curr_route[:]
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        
       
        new_len = calculate_total_dist(new_route, dist_matrix)
        
        # QUANTUM TUNNELING CRITERION (Metropolis)
        # 1. If new state is lower energy (better), accept it.
        # 2. If new state is higher energy (worse), accept it with probability P = exp(-dE/T)
        if new_len < curr_len or np.random.rand() < np.exp((curr_len - new_len) / temperature):
            curr_route = new_route
            curr_len = new_len
            if curr_len < best_len:
                best_len = curr_len
                best_route = curr_route
                
    return [nodes[i] for i in best_route]

def solve_hybrid_quantum(start_node, stops_data):
   
    all_nodes = [start_node] + stops_data
    n = len(all_nodes)
    
  
    if n < 10: 
        return simulated_quantum_annealing(all_nodes)
    
    # --- HYBRID STEP: K-MEANS CLUSTERING ---
    coords = [[s['coords'][0], s['coords'][1]] for s in stops_data]
    k = max(1, n // 5) # Adaptive cluster size
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(coords)
    
    clusters = {i: [] for i in range(k)}
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(stops_data[idx])
        
    final_route = [start_node]
    sorted_cluster_indices = sorted(clusters.keys())
    
    for cluster_idx in sorted_cluster_indices:
        sub_stops = clusters[cluster_idx]
        if not sub_stops: continue
        optimized_sub = simulated_quantum_annealing([final_route[-1]] + sub_stops)
        final_route.extend(optimized_sub[1:])
        
    return final_route
