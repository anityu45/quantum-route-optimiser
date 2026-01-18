# ⚛️ Quantum Logistics Pro
### *Physics-Inspired Route Optimization for Next-Gen Supply Chains*

**Quantum Logistics Pro** is a high-performance logistics engine that solves the Traveling Salesman Problem (TSP) using **Simulated Quantum Annealing**. By modeling delivery routes as "energy states," the system uses simulated tunneling to escape local minima, finding more efficient paths than traditional greedy algorithms.

---

## 📺 User Interface & Workflow

The UI is built with a **Cyberpunk-Dark Aesthetic** using Streamlit, designed to provide dispatchers with a high-tech "command center" feel.

### 1. Data Input & Ingestion
* **Search Integration:** Uses the `geopy` and `Nominatim` API for real-time location autocompletion.
* **Bulk Upload:** Supports CSV ingestion (as seen in `demo_stops.csv`) for massive datasets.
* **Fleet Configuration:** Adjust vehicle count, fuel prices, and vehicle mileage to calculate real-world ROI.

> **[INSERT SCREENSHOT: SIDEBAR_INPUT_WORKFLOW]**
> *Description: Sidebar showing the location search and fleet parameter sliders.*

### 2. The Optimization Engine
* **Live Simulation:** When "RUN" is clicked, the system initializes a "Quantum Tunneling Simulation." 
* **Convergence Monitoring:** A live "Energy Landscape" chart (via `st.line_chart`) shows the algorithm finding lower-cost routes in real-time.

> **[INSERT SCREENSHOT: OPTIMIZATION_DASHBOARD]**
> *Description: The main dashboard showing the energy convergence graph and the 'Tunneling Events' metric.*

### 3. Geospatial Visualization
* **Interactive Maps:** Powered by `Folium`, the app renders real-road geometry.
* **Multi-Vehicle Support:** Each vehicle route is color-coded and assigned a unique ID for clear dispatcher visibility.

> **[INSERT SCREENSHOT: ROUTE_MAP_VIEW]**
> *Description: Folium map showing color-coded road paths for multiple delivery vehicles.*

---

## ⚙️ Backend Architecture (Function-by-Function)

The backend is modularized to separate the physics-inspired math from the API handling.

### `app.py`: The Quantum Core
* **`build_matrices(nodes)`**: 
    * *Use Case:* Converts a list of GPS coordinates into a Distance and Time matrix. 
    * *Logic:* It queries the **OSRM Table API** to get real road distances instead of "as-the-crow-flies" math.
* **`calculate_energy(route, ...)`**: 
    * *Use Case:* The "Objective Function." 
    * *Logic:* Calculates total distance + penalties for late deliveries (Time Window violations). Lower energy = better route.
* **`solve_hybrid_quantum(...)`**: 
    * *Use Case:* The main solver. 
    * *Logic:* Orchestrates K-Means clustering for fleet splitting and runs the Annealing algorithm on each cluster.

### `api.py`: External Integrations
* **`get_road_path(coords)`**: 
    * *Use Case:* Pathfinding.
    * *Logic:* A multi-tier fallback system. It first tries **TomTom API** (for traffic-aware routing), falls back to **OSRM**, and finally uses straight lines if offline.
* **`search_places(search_term)`**: 
    * *Use Case:* UI Searchbox.
    * *Logic:* Connects the frontend search bar to the OpenStreetMap database.

### `logic.py`: Benchmarking & Orchestration
* **`run_benchmark_suite(...)`**: 
    * *Use Case:* Competitive Analysis.
    * *Logic:* Simultaneously runs **Nearest Neighbor**, **2-opt**, and the **Quantum Solver**. It calculates the "Improvement %" to prove the Quantum solver's superiority.

---

## 🛠️ Installation & Setup

1. **Clone the Project**
   ```bash
   git clone [https://github.com/your-username/quantum-logistics.git](https://github.com/your-username/quantum-logistics.git)
   cd quantum-logistics
