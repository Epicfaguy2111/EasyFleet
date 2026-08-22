# EasyFleet
The application will plot the most optimal route for the fleet while gathering data and updating the statistics such as fuel consumption and etas while keeping the relevant supervisors in the loop

# Workspace
easyfleet/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (vehicles, drivers, routes, ai)
│   │   ├── core/         # Config, security, database sessions
│   │   ├── models/       # SQLAlchemy / SQLModel database tables
│   │   ├── schemas/      # Pydantic validation schemas
│   │   └── services/     # Route optimization, AI analytics, alerts
│   ├── pyproject.toml
│   └── main.py
└── frontend/
    ├── src/
    │   ├── components/   # Mapbox/Leaflet views, Recharts telemetry
    │   ├── pages/        # Dashboard, Fleet, Drivers, Alerts
    │   └── services/     # API clients
    └── package.json
    
# Scope
Programming aspect
Backend 
Python Fast API 
What the AI will do:
    • Optimize routes
    • Predictive maintenance 
    • Assist in event of a Emergency
    • Driving irregularities 
        ◦ Harsh breaking
        ◦ Idling
        ◦ Patterns regarding fuel theft
    • A AI Assistant for management
Frontend dashboard
    • Map view
        ◦ Mapbox
        ◦ Leaflet
    • Charts for fuel efficiency, downtime cost per km
        ◦ Recharts 
        ◦ Charts.js
The stats regarding the application
    • The vehicles will require multiple sensors like 
        ◦ Vehicle statistics
            ▪ Make and model
            ▪ Age
            ▪ location 
            ▪ speed 
            ▪ assumed fuel consumptions – this can be acquired from eith historical data or the value can be fetched from a online source
        ◦ expected and current expenses
        ◦ Stats regarding emergencies
            ▪ High risk areas
            ▪ Known vehicle issues 
        ◦ scheduled activities 
            ▪ vehicle maintenance and petrol activities
        ◦ Driver statistics
            ▪ Personal details 
                • Name surname age height etc
            ▪ Driver history 
            ▪ Job status
                • Job title 
                • Employment status
        ◦ Product description
            ▪ Shipment ID
            ▪ Shipment eta 
            ▪ End Location

# Core Data Models

    Vehicles: id, make_model, year, vin, current_lat, current_lon, speed, baseline_fuel_consumption, status (active, maintenance, idle).

    Telemetry & Sensors: id, vehicle_id, timestamp, fuel_level, engine_temp, harsh_braking_events, idle_duration_minutes.

    Drivers: id, name, surname, license_number, employment_status, assigned_vehicle_id, safety_score.

    Shipments & Routes: id, shipment_code, driver_id, vehicle_id, origin_coords, destination_coords, current_eta, route_geometry, status.

    Alerts & Incidents: id, vehicle_id, driver_id, alert_type (fuel theft anomaly, high-risk zone entry, collision, maintenance warning), severity, resolved_status.

# Running

http://127.0.0.1:8000/frontend/HTML/index.html

source .venv/bin/activate
uvicorn main:app --app-dir backend --reload


# Clearing Databases

rm -f drivers.db easyfleet.db backend/data/drivers.db backend/data/easyfleet.db backend/drivers.db backend/easyfleet.db