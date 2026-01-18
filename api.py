# api.py
import requests
import streamlit as st
from geopy.geocoders import Nominatim

# Optional: Add TomTom Key if available, otherwise it uses OSRM (Free)
TOMTOM_API_KEY = "L4gkmNxotmMVp8KJ74X05dNffs2E1G55"  

@st.cache_data(ttl=3600)
def search_places(search_term: str):
    """Autocomplete search function."""
    if not search_term: return []
    agent_id = st.session_state.get('user_agent_id', 'unknown')
    geolocator = Nominatim(user_agent=f"quantum_logistics_{agent_id}")
    try:
        locations = geolocator.geocode(search_term, exactly_one=False, limit=5, timeout=4)
        if locations:
            return [(loc.address, {"name": loc.address, "coords": (loc.latitude, loc.longitude)}) for loc in locations]
        return []
    except Exception:
        return []

def get_road_path(coords):
    """
    Fetches real road geometry.
    Priority: TomTom -> OSRM -> Straight Line (Fallback)
    """
    if len(coords) < 2: return None, 0, 0
    
    # 1. Try TomTom (High Accuracy)
    if TOMTOM_API_KEY:
        try:
            loc_string = ":".join([f"{lat},{lon}" for lat, lon in coords])
            url = f"https://api.tomtom.com/routing/1/calculateRoute/{loc_string}/json"
            params = {"key": TOMTOM_API_KEY, "traffic": "true", "routeType": "fastest"}
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                routes = data.get("routes", [])
                if routes:
                    summary = routes[0]["summary"]
                    legs = routes[0]["legs"]
                    points = []
                    for leg in legs:
                        for p in leg["points"]:
                            points.append([p["latitude"], p["longitude"]])
                    return points, summary["lengthInMeters"] / 1000, summary["travelTimeInSeconds"] / 60
        except Exception:
            pass

    # 2. Try OSRM (Open Source / Free)
    loc_string = ";".join([f"{lon},{lat}" for lat, lon in coords])
    url = f"http://router.project-osrm.org/route/v1/driving/{loc_string}?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if 'routes' in data and len(data['routes']) > 0:
                rt = data['routes'][0]
                geometry = rt['geometry']['coordinates']
                # OSRM returns [lon, lat], Folium needs [lat, lon]
                path_geo = [[p[1], p[0]] for p in geometry]
                return path_geo, rt['distance'] / 1000, rt['duration'] / 60
    except Exception:
        pass

    # 3. Fallback to Straight Lines
    return coords, 0, 0
