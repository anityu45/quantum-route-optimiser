import requests
import polyline

def get_osrm_route(coordinates):
    locs = ";".join([f"{lon},{lat}" for lat, lon in coordinates])
    
    url = f"http://router.project-osrm.org/route/v1/driving/{locs}?overview=full&geometries=polyline"
    
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None, 0, 0
        data = r.json()
        route = data['routes'][0]
        points = polyline.decode(route['geometry'])
        distance_km = route['distance'] / 1000
        duration_min = route['duration'] / 60
        return points, distance_km, duration_min
    except Exception as e:
        print(f"Routing Error: {e}")
        return None, 0, 0