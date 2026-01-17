from geopy.distance import geodesic

def solve_simple_route(start_node, stops_data):
    """
    Finds the nearest next stop. Fast and crash-proof.
    """
    route = [start_node]
    unvisited = stops_data[:] 
    current_node = start_node

    while unvisited:
        # Find the closest next stop
        next_stop = min(unvisited, key=lambda x: geodesic(current_node['coords'], x['coords']).km)
        route.append(next_stop)
        unvisited.remove(next_stop)
        current_node = next_stop

    return route