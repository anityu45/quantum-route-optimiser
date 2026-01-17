# quantum-route-optimiser
Hybrid Quantum-Classical solver for logistics routing. utilizing Metropolis-Hastings algorithms and Scikit-Learn to optimize delivery paths, visualize real-time traffic data, and reduce fuel costs. Built with Python &amp; Streamlit.

# Quantum Logistics Optimizer

**Automated Route Planning for Last-Mile Delivery**

## Project Overview
We built this project to solve a common problem in logistics: inefficient delivery routes. When a driver has 10 or more stops, figuring out the perfect order to visit them is incredibly difficult for a human. This leads to wasted fuel and late deliveries.

Our application automates this process. It takes a list of delivery locations and uses a pathfinding algorithm to calculate the shortest, most efficient route connecting them all.

## How It Works
Instead of simply connecting point A to point B, our system analyzes the entire batch of locations. It uses a "Simulated Annealing" approach—a technique inspired by physics—to shuffle the order of stops until it finds a path that minimizes total travel distance.

## Key Features
- **Route Optimization:** Instantly reorders messy delivery lists into a clean, logical path.
- **Interactive Mapping:** Visualizes the route on a dark-mode map for easy tracking.
- **CSV Upload:** Users can upload bulk data directly instead of entering addresses manually.
- **Performance Metrics:** Real-time calculation of total distance and estimated travel time.

## How to Run This Project

1.  **Install Dependencies**
    Run the following command to install the necessary Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Application**
    Launch the interface using Streamlit:
    ```bash
    streamlit run main.py
    ```

3.  **Test with Data**
    We have included a file named `demo_data.csv`. Upload this file in the sidebar to see the optimization in action.

## Technologies Used
- **Python:** Core logic and calculation.
- **Streamlit:** User interface and frontend.
- **Folium:** Map rendering and visualization.
- **Geopy:** Distance calculations.

---
*Created for the Hackathon 2026*
