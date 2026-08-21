// ===============================
// MAP SETUP
// ===============================

const map = L.map("map").setView([-33.9249, 18.4241], 10);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

let routeLayerGroup = L.layerGroup().addTo(map);

// ===============================
// PROFILE STATE
// ===============================

let truckProfiles = [];
let selectedProfile = null;

// ===============================
// DYNAMIC LEGAL LIMITS UI
// ===============================

const vehicleTypeSelect = document.getElementById("newVehicleType");
if (vehicleTypeSelect) {
    vehicleTypeSelect.addEventListener("change", function () {
        const limitText = document.getElementById("dimensionLimitText");
        const lengthLimit = document.getElementById("lengthLimit");
        if (this.value === "single_rigid") {
            limitText.textContent = "Single Rigid max length: 12.5m, Width: 2.6m, Height: 4.3m";
            lengthLimit.textContent = "Maximum: 12.5 m";
        } else if (this.value === "articulated") {
            limitText.textContent = "Articulated max length: 18.5m, Width: 2.6m, Height: 4.3m";
            lengthLimit.textContent = "Maximum: 18.5 m";
        } else if (this.value === "other_combination") {
            limitText.textContent = "Combination max length: 22.0m, Width: 2.6m, Height: 4.3m";
            lengthLimit.textContent = "Maximum: 22.0 m";
        } else {
            limitText.textContent = "Select a vehicle type to view the applicable limits.";
            lengthLimit.textContent = "Select vehicle type first.";
        }
    });
}

// ===============================
// LOAD PROFILES
// ===============================

async function loadProfiles() {
    try {
        const response = await fetch("http://127.0.0.1:8000/trucks/");
        if (response.ok) {
            truckProfiles = await response.json();
        }
    } catch (err) {
        console.warn("Could not load from API, falling back to local cache:", err);
        const savedProfiles = localStorage.getItem("truckProfiles");
        if (savedProfiles) {
            truckProfiles = JSON.parse(savedProfiles);
        }
    }

    updateProfileDropdown();
}

// ===============================
// UPDATE DROPDOWN
// ===============================

function updateProfileDropdown() {
    const dropdown = document.getElementById("truckProfile");
    dropdown.innerHTML = `<option value="">-- Select Truck Profile --</option>`;

    truckProfiles.forEach(profile => {
        const option = document.createElement("option");
        option.value = profile.id;
        option.textContent = `${profile.fleet_number || profile.name} - ${profile.registration}`;
        dropdown.appendChild(option);
    });
}

// ===============================
// PROFILE SELECTED
// ===============================

document.getElementById("truckProfile").addEventListener("change", function () {
    const profileId = this.value;

    if (!profileId) {
        selectedProfile = null;
        document.getElementById("truckInfoPanel").style.display = "none";
        return;
    }

    selectedProfile = truckProfiles.find(profile => profile.id == profileId);
    displayProfile(selectedProfile);
});

// ===============================
// DISPLAY PROFILE
// ===============================

function displayProfile(profile) {
    if (!profile) return;
    document.getElementById("truckInfoPanel").style.display = "block";

    document.getElementById("truckName").textContent = profile.name || "--";
    document.getElementById("truckFleetNumber").textContent = profile.fleet_number || "--";
    document.getElementById("truckVin").textContent = profile.vin || "--";
    document.getElementById("truckMake").textContent = profile.make || "--";
    document.getElementById("truckModel").textContent = profile.model || "--";
    document.getElementById("truckYear").textContent = profile.year || "--";
    document.getElementById("truckFuelType").textContent = (profile.fuel_type || "--").toUpperCase();
    document.getElementById("truckStatus").textContent = (profile.status || "--").replace("_", " ").toUpperCase();
    document.getElementById("truckWeight").textContent = `${Number(profile.weight || 0).toLocaleString()} kg`;
    document.getElementById("truckPayload").textContent = `${Number(profile.payload || 0).toLocaleString()} kg`;
    document.getElementById("truckEnginePower").textContent = `${profile.engine_power || 0} kW`;
    document.getElementById("truckFuel").textContent = `${profile.fuel || 0} L`;
    document.getElementById("truckAxles").textContent = profile.axles || "--";
    document.getElementById("truckVehicleType").textContent = (profile.vehicle_type || "--").replace("_", " ");
    document.getElementById("truckLength").textContent = `${profile.length || 0} m`;
    document.getElementById("truckWidth").textContent = `${profile.width || 0} m`;
    document.getElementById("truckHeight").textContent = `${profile.height || 0} m`;
    document.getElementById("truckOdometer").textContent = `${Number(profile.odometer || 0).toLocaleString()} km`;
    document.getElementById("truckNextService").textContent = profile.next_service_km ? `${Number(profile.next_service_km).toLocaleString()} km` : "--";
}

// ===============================
// CREATE PROFILE MODAL
// ===============================

const modal = document.getElementById("profileModal");

document.getElementById("createProfileButton").addEventListener("click", () => {
    modal.style.display = "flex";
});

document.getElementById("closeModalButton").addEventListener("click", closeModal);
document.getElementById("cancelProfileButton").addEventListener("click", closeModal);

function closeModal() {
    modal.style.display = "none";
}

// ===============================
// SAVE PROFILE
// ===============================

document.getElementById("saveProfileButton").addEventListener("click", saveProfile);

async function saveProfile() {
    const payload = {
        name: document.getElementById("newTruckName").value.trim(),
        fleet_number: document.getElementById("newFleetNumber").value.trim(),
        registration: document.getElementById("newRegistration").value.trim(),
        vin: document.getElementById("newVin").value.trim(),
        make: document.getElementById("newMake").value.trim(),
        model: document.getElementById("newModel").value.trim(),
        year: Number(document.getElementById("newYear").value),
        fuel_type: document.getElementById("newFuelType").value,
        vehicle_type: document.getElementById("newVehicleType").value,
        axles: Number(document.getElementById("newAxleCount").value),
        engine_power: Number(document.getElementById("newEnginePower").value),
        weight: Number(document.getElementById("newWeight").value),
        payload: Number(document.getElementById("newPayload").value),
        fuel: Number(document.getElementById("newFuel").value),
        length: Number(document.getElementById("newLength").value),
        width: Number(document.getElementById("newWidth").value),
        height: Number(document.getElementById("newHeight").value),
        odometer: Number(document.getElementById("newOdometer").value),
        status: document.getElementById("newStatus").value,
        last_service_date: document.getElementById("newLastService").value || null,
        next_service_km: document.getElementById("newNextService").value ? Number(document.getElementById("newNextService").value) : null
    };

    if (!payload.name || !payload.vin || payload.vin.length !== 17 || !payload.registration) {
        alert("Please ensure all required fields are filled correctly (VIN must be exactly 17 characters).");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/trucks/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to save truck profile");
        }

        const savedTruck = await response.json();
        truckProfiles.push(savedTruck);
        localStorage.setItem("truckProfiles", JSON.stringify(truckProfiles));
        updateProfileDropdown();

        document.getElementById("truckProfile").value = savedTruck.id;
        selectedProfile = savedTruck;
        displayProfile(savedTruck);

        closeModal();
        clearProfileForm();
    } catch (err) {
        console.error("Error saving truck:", err);
        alert(`Error: ${err.message}`);
    }
}

// ===============================
// CLEAR PROFILE FORM
// ===============================

function clearProfileForm() {
    document.getElementById("newTruckName").value = "";
    document.getElementById("newFleetNumber").value = "";
    document.getElementById("newRegistration").value = "";
    document.getElementById("newVin").value = "";
    document.getElementById("newMake").value = "";
    document.getElementById("newModel").value = "";
    document.getElementById("newYear").value = "";
    document.getElementById("newFuelType").value = "";
    document.getElementById("newVehicleType").value = "";
    document.getElementById("newAxleCount").value = "2";
    document.getElementById("newEnginePower").value = "";
    document.getElementById("newWeight").value = "";
    document.getElementById("newPayload").value = "";
    document.getElementById("newFuel").value = "";
    document.getElementById("newLength").value = "";
    document.getElementById("newWidth").value = "";
    document.getElementById("newHeight").value = "";
    document.getElementById("newOdometer").value = "";
    document.getElementById("newStatus").value = "active";
    document.getElementById("newLastService").value = "";
    document.getElementById("newNextService").value = "";
}

// ===============================
// CALCULATE ROUTE
// ===============================

document.getElementById("routeButton").addEventListener("click", calculateRoute);

async function calculateRoute() {
    const start = document.getElementById("start").value.trim();
    const destination = document.getElementById("destination").value.trim();
    const driverName = document.getElementById("driverName").value.trim();

    if (!selectedProfile) {
        alert("Please select a truck profile.");
        return;
    }

    if (!start || !destination) {
        alert("Please enter a starting location and destination.");
        return;
    }

    const routeRequest = {
        start: start,
        destination: destination,
        truck: {
            name: selectedProfile.name,
            registration: selectedProfile.registration,
            weight: selectedProfile.weight,
            height: selectedProfile.height,
            length: selectedProfile.length,
            fuel: selectedProfile.fuel
        },
        driver: {
            name: driverName || "Unassigned",
            licence: document.getElementById("driverLicence").value,
            phone: document.getElementById("driverPhone").value,
            drivingHours: parseFloat(document.getElementById("driverHours").value) || 9.0
        }
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/route", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(routeRequest)
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const route = await response.json();

        document.getElementById("distance").textContent = `${route.distance_km} km`;
        document.getElementById("duration").textContent = route.duration_text;
        document.getElementById("fuelRequired").textContent = `${route.fuel_required_liters} L`;

        drawRoute(route);
    } catch (err) {
        console.error("Error calculating route:", err);
        alert("Failed to calculate route. Ensure FastAPI backend is running.");
    }
}

function drawRoute(route) {
    routeLayerGroup.clearLayers();

    const startMarker = L.marker(route.start_coord).bindPopup(`<b>Start:</b> Origin`);
    const destMarker = L.marker(route.dest_coord).bindPopup(`<b>Destination:</b> Destination`);
    const polyline = L.polyline(route.waypoints, { color: '#2563eb', weight: 5 });

    routeLayerGroup.addLayer(startMarker);
    routeLayerGroup.addLayer(destMarker);
    routeLayerGroup.addLayer(polyline);

    map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
}

// ===============================
// START APPLICATION
// ===============================

loadProfiles();