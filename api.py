from geopy.distance import geodesic

def get_route_shape(coordinates):
    
    path_points = coordinates
    
    # 2. Calculate Total Distance (Sum of straight lines)
    total_dist_km = 0
    for i in range(len(coordinates) - 1):
        # Calculate distance between point i and i+1 using geopy
        dist = geodesic(coordinates[i], coordinates[i+1]).km
        total_dist_km += dist
        
    # 3. Estimate Time (Assume average speed of 60 km/h)
    # Time = Distance / Speed * 60 minutes
    total_time_min = (total_dist_km / 60) * 60
    
    return path_points, total_dist_km, total_time_min