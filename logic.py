# logic.py
import app as quantum_solver

def optimize_route_algo(start, stops, round_trip=False):
    """
    Router Logic.
    Strictly calls the Hybrid Quantum Solver.
    NO Classical OR-Tools allowed.
    """
    # 1. Execute Quantum-Inspired Optimization
    sorted_nodes = quantum_solver.solve_hybrid_quantum(start, stops)
    
    # 2. Handle Round Trip (Return to Warehouse)
    if round_trip:
        sorted_nodes.append(sorted_nodes[0])
        
    return sorted_nodes
