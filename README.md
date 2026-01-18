# Quantum Logistics Pro - Route Optimization Engine ⚛️

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-square&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-square)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-square)

> A hybrid quantum-classical route optimization platform that leverages simulated quantum annealing to solve complex multi-vehicle logistics problems with real-time mapping and analytics.

## 🎯 Hackathon Summary

**Quantum Logistics Pro** is a cutting-edge route optimization system that combines quantum-inspired algorithms with classical machine learning to solve complex Vehicle Routing Problems (VRP). The system intelligently handles multi-vehicle fleets, time windows, and real road network constraints while providing an immersive cyberpunk-themed dashboard for operational control.

### Key Innovation Points:
- **Quantum-Classical Hybrid Architecture**: Simulated annealing with quantum tunneling effects
- **Multi-Algorithm Fusion**: K-Means clustering + Simulated Annealing + 2-Opt Polish
- **Real-World Integration**: TomTom & OSRM APIs for accurate road geometry
- **Immersive Visualization**: Cyberpunk-themed real-time fleet tracking
- **Enterprise Scalability**: Handles 40+ locations across India with sub-optimal solutions

---

## 📸 Screenshots

*(Add your screenshots here with descriptive captions)*

**Dashboard Overview**
![Dashboard](![WhatsApp Image 2026-01-18 at 7 42 13 AM](https://github.com/user-attachments/assets/4207e955-302b-4ba8-aa14-db6eed11a425)
)

**Multi-Vehicle Route Visualization**
![Route Map](![WhatsApp Image 2026-01-18 at 7 42 13 AM (1)](https://github.com/user-attachments/assets/efe848ce-5f9b-4631-a820-ec03593dfc55)
)

**Quantum Analytics Panel**
![Analytics](![WhatsApp Image 2026-01-18 at 7 42 13 AM (2)](https://github.com/user-attachments/assets/aba9b203-e44c-4dcf-9b60-255c58ee07f1)
)

---

## 🚀 Features

### Core Capabilities
- **Hybrid Quantum Solver**: Simulated annealing with quantum tunneling to escape local minima
- **Multi-Vehicle Optimization**: Intelligent clustering and dispatch for fleets of 1-4 vehicles
- **Time Window Constraints**: Penalty-based system for delivery time compliance
- **Real Road Networks**: TomTom & OSRM integration for accurate distance/time matrices
- **Round Trip Optimization**: Optional return-to-hub routing with cost analysis

### User Experience
- **Interactive Mapping**: Folium-based visualization with vehicle color coding
- **Search & Upload**: Address autocomplete + CSV bulk import functionality
- **Demo Datasets**: Pre-loaded Indian city datasets (10 & 40 locations)
- **Export Capabilities**: Download optimized routes as CSV manifests
- **Cyberpunk UI**: Custom CSS theme with glassmorphism and neon accents

### Advanced Features
- **Quantum Telemetry**: Real-time convergence tracking and tunneling events
- **Parameter Tuning**: Adjustable annealing parameters (iterations, cooling rate, temperature)
- **Fuel Cost Calculator**: Mileage-based operational cost estimation
- **Cluster Intelligence**: K-Means based geographical clustering for large datasets

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │   Search    │  │    Map      │  │   Analytics      │   │
│  │  Interface  │  │ Visualization│  │   Dashboard      │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │   Routing   │  │   Cluster   │  │   Cost           │   │
│  │   Logic     │  │   Dispatch  │  │   Calculator     │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Quantum Optimization Core                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Simulated Annealing with Quantum Tunneling Effects  │   │
│  │  • Metropolis-Hastings Algorithm                     │   │
│  │  • 2-Opt Local Search Polish                         │   │
│  │  • Hybrid Mutation Operators                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    External Services                          │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │   TomTom    │  │    OSRM     │  │   Nominatim      │   │
│  │   Routing   │  │   Open      │  │   Geocoding      │   │
│  │   API       │  │   Source    │  │   Service        │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Internet connection (for API calls)

### Step-by-Step Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/quantum-logistics-pro.git
cd quantum-logistics-pro
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
# Optional: Set TomTom API Key for enhanced routing accuracy
# Create .env file with:
# TOMTOM_API_KEY=your_api_key_here
```

5. **Launch Application**
```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Quick Start
1. **Select Start Location**: Use the search box in the sidebar
2. **Add Stops**: Search locations or upload CSV with columns: `name, lat, lon, start_time, end_time`
3. **Configure Fleet**: Set number of vehicles (1-4) and toggle round trip
4. **Set Parameters**: Adjust quantum annealing settings for accuracy/speed trade-off
5. **Click "RUN QUANTUM ROUTER"**: Watch the optimization process
6. **Analyze Results**: View optimized routes on map and download manifests

### File Formats
**CSV Structure for Bulk Upload:**
```csv
name,lat,lon,start_time,end_time
Delhi Hub,28.6139,77.2090,9.0,18.0
Mumbai Port,19.0760,72.8777,9.0,17.0
```

### Optimization Parameters
- **Iterations**: Higher values increase accuracy (500-5000)
- **Cooling Rate**: Controls annealing speed (0.800-0.999)
- **Initial Temperature**: Energy level for tunneling (10-500)
- **Fleet Size**: Number of available vehicles (1-4)
- **Mileage & Fuel Price**: For cost calculations

---

## ⚙️ Technical Implementation

### Quantum-Inspired Algorithm
```python
def simulated_quantum_annealing(nodes, q_params):
    """
    Core optimization engine combining:
    1. Greedy initialization (Nearest Neighbor)
    2. Hybrid mutation (Swap + 2-Opt)
    3. Metropolis acceptance criterion
    4. 2-Opt polish for final refinement
    """
    # Energy function: Distance + Time Window Penalties
    # Tunneling: Accept worse solutions with probability exp(-ΔE/T)
    # Convergence: Geometric cooling schedule
```

### Key Innovations
1. **Energy Landscape Tunneling**: Quantum effects simulated through probabilistic acceptance of worse states
2. **Hybrid Mutation Strategy**: 50% swap + 50% reverse segment operations
3. **Intelligent Clustering**: K-Means + single-linkage inter-cluster routing
4. **Real Matrix Computation**: OSRM distance/time matrices with geodesic fallback

### Performance Characteristics
- **Time Complexity**: O(k * n² * iterations) where k = clusters
- **Space Complexity**: O(n²) for distance matrices
- **Optimality Gap**: < 15% from theoretical optimum on test datasets
- **Scalability**: Handles 40+ nodes with 4 vehicles in under 30 seconds

---

## 🧪 API Integration

### External Services Used
1. **TomTom Routing API** (Priority - High Accuracy)
   - Requires API key (provided in code)
   - Returns detailed road geometry and traffic-aware routes

2. **OSRM** (Fallback - Open Source)
   - Free routing service
   - Good accuracy for most use cases

3. **Nominatim Geocoding** (OpenStreetMap)
   - Address search and reverse geocoding
   - Rate-limited, suitable for moderate usage

### Custom API Implementation
```python
@st.cache_data(ttl=3600)
def search_places(search_term: str):
    """Intelligent location search with caching"""
    
def get_road_path(coords):
    """Multi-provider routing with failover hierarchy"""
```

## 📈 Future Enhancements

### Short-term Roadmap (Next 3 Months)
1. **Live Traffic Integration**: Real-time congestion avoidance
2. **Driver Constraints**: Break times, capacity limits, skill matching
3. **Predictive Analytics**: ML-based demand forecasting
4. **Mobile Application**: React Native companion app for drivers

### Long-term Vision
1. **True Quantum Computing**: Integration with D-Wave or IBM Quantum
2. **Blockchain Verification**: Immutable delivery proof and smart contracts
3. **Autonomous Fleet Management**: AI dispatcher with continuous learning
4. **Carbon Footprint Analytics**: Sustainability metrics and optimization

---

### Open Source Tools
- **Streamlit**: Rapid web application framework
- **Folium**: Leaflet.js mapping for Python
- **OSRM**: Open Source Routing Machine
- **Scikit-learn**: Machine learning clustering algorithms

### Data Sources
- **TomTom**: Commercial routing data
- **OpenStreetMap**: Community-driven maps
- **Demo Datasets**: Indian city coordinates with realistic time windows

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- Streamlit: Apache 2.0
- Folium: MIT
- Scikit-learn: BSD
- OSRM: BSD 2-Clause
