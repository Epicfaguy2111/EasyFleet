// ===============================
// MAP
// ===============================

const map = L.map("map").setView(
    [-33.9249, 18.4241],
    10
);


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "&copy; OpenStreetMap contributors"
    }
).addTo(map);


// ===============================
// PROFILE DATA
// ===============================

let truckProfiles = [];

let selectedProfile = null;


// ===============================
// LEGAL DIMENSIONAL LIMITS
// ===============================

const legalLimits = {

    single_rigid: {
        length: 12.5,
        width: 2.6,
        height: 4.3
    },

    articulated: {
        length: 18.5,
        width: 2.6,
        height: 4.3
    },

    other_combination: {
        length: 22.0,
        width: 2.6,
        height: 4.3
    }

};


// ===============================
// LOAD PROFILES
// ===============================

async function loadProfiles() {

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/trucks/"
            );


        if (response.ok) {

            const data =
                await response.json();


            truckProfiles = data.map(truck => ({

                // ==========================
                // IDENTIFICATION
                // ==========================

                id:
                    truck.id,

                vin:
                    truck.vin || "",

                fleetNumber:
                    truck.fleet_number || "",

                name:
                    truck.name || "",

                registration:
                    truck.registration || "",

                make:
                    truck.make || "",

                model:
                    truck.model || "",

                year:
                    truck.year ?? null,


                // ==========================
                // ENGINE / VEHICLE
                // ==========================

                fuelType:
                    truck.fuel_type || "diesel",

                grossVehicleWeightKg:
                    truck.gross_vehicle_weight_kg ?? 0,

                payloadCapacityKg:
                    truck.payload_capacity_kg ?? 0,

                enginePowerKw:
                    truck.engine_power_kw ?? 0,

                fuelTankCapacityL:
                    truck.fuel_tank_capacity_l ?? 0,

                axleCount:
                    truck.axle_count ?? 2,


                // ==========================
                // VEHICLE TYPE
                // ==========================

                vehicleType:
                    truck.vehicle_type || "single_rigid",


                // ==========================
                // DIMENSIONS
                // ==========================

                lengthM:
                    truck.length_m ??
                    truck.length ??
                    0,

                widthM:
                    truck.width_m ??
                    truck.width ??
                    0,

                heightM:
                    truck.height_m ??
                    truck.height ??
                    0,


                // ==========================
                // OPERATION
                // ==========================

                odometerKm:
                    truck.odometer_km ?? 0,

                status:
                    truck.status || "active",

                lastServiceDate:
                    truck.last_service_date || null,

                nextServiceDueKm:
                    truck.next_service_due_km ?? null

            }));

        }

    }

    catch (err) {

        console.warn(
            "Could not load from API, falling back to local cache:",
            err
        );


        const savedProfiles =
            localStorage.getItem(
                "truckProfiles"
            );


        if (savedProfiles) {

            truckProfiles =
                JSON.parse(savedProfiles);

        }

    }


    updateProfileDropdown();
}


// ===============================
// UPDATE DROPDOWN
// ===============================

function updateProfileDropdown() {

    const dropdown =
        document.getElementById("truckProfile");


    dropdown.innerHTML = `
        <option value="">
            -- Select Truck Profile --
        </option>
    `;


    truckProfiles.forEach(profile => {

        const option =
            document.createElement("option");


        option.value =
            profile.id;


        option.textContent =
            `${profile.name} - ${profile.registration}`;


        dropdown.appendChild(option);

    });

}


// ===============================
// PROFILE SELECTED
// ===============================

document
    .getElementById("truckProfile")
    .addEventListener(
        "change",
        function () {

            const profileId =
                this.value;


            if (!profileId) {

                selectedProfile = null;


                document
                    .getElementById("truckInfoPanel")
                    .style.display = "none";


                return;
            }


            selectedProfile =
                truckProfiles.find(
                    profile =>
                        profile.id == profileId
                );


            if (selectedProfile) {

                displayProfile(
                    selectedProfile
                );

            }

        }
    );


// ===============================
// DISPLAY PROFILE
// ===============================

function displayProfile(profile) {

    if (!profile) {
        return;
    }


    document
        .getElementById("truckInfoPanel")
        .style.display = "block";


    setText(
        "truckName",
        profile.name
    );


    setText(
        "truckFleetNumber",
        profile.fleetNumber || "--"
    );


    setText(
        "truckVin",
        profile.vin || "--"
    );


    setText(
        "truckMake",
        profile.make || "--"
    );


    setText(
        "truckModel",
        profile.model || "--"
    );


    setText(
        "truckYear",
        profile.year || "--"
    );


    setText(
        "truckFuelType",
        formatEnum(profile.fuelType)
    );


    setText(
        "truckStatus",
        formatEnum(profile.status)
    );


    setText(
        "truckWeight",
        formatNumber(
            profile.grossVehicleWeightKg
        ) + " kg"
    );


    setText(
        "truckPayload",
        formatNumber(
            profile.payloadCapacityKg
        ) + " kg"
    );


    setText(
        "truckEnginePower",
        formatNumber(
            profile.enginePowerKw
        ) + " kW"
    );


    setText(
        "truckFuel",
        formatNumber(
            profile.fuelTankCapacityL
        ) + " L"
    );


    setText(
        "truckAxles",
        profile.axleCount || "--"
    );


    setText(
        "truckVehicleType",
        formatEnum(profile.vehicleType)
    );


    setText(
        "truckLength",
        `${profile.lengthM || 0} m`
    );


    setText(
        "truckWidth",
        `${profile.widthM || 0} m`
    );


    setText(
        "truckHeight",
        `${profile.heightM || 0} m`
    );


    setText(
        "truckOdometer",
        formatNumber(
            profile.odometerKm
        ) + " km"
    );


    setText(
        "truckNextService",
        profile.nextServiceDueKm !== null &&
        profile.nextServiceDueKm !== undefined
            ? formatNumber(
                profile.nextServiceDueKm
            ) + " km"
            : "Not set"
    );

}


// ===============================
// HELPER FUNCTIONS
// ===============================

function setText(id, value) {

    const element =
        document.getElementById(id);


    if (element) {

        element.textContent =
            value ?? "--";

    }

}


function formatNumber(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "--";

    }


    return Number(value).toLocaleString();

}


function formatEnum(value) {

    if (!value) {

        return "--";

    }


    return value
        .replace(/_/g, " ")
        .replace(/\b\w/g, char =>
            char.toUpperCase()
        );

}



// ===============================
// CREATE PROFILE MODAL
// ===============================

const modal =
    document.getElementById("profileModal");


document
    .getElementById("createProfileButton")
    .addEventListener(
        "click",
        function () {

            modal.style.display = "flex";

            updateDimensionLimits();

            document
                .getElementById("newTruckName")
                .focus();

        }
    );


document
    .getElementById("closeModalButton")
    .addEventListener(
        "click",
        closeModal
    );


document
    .getElementById("cancelProfileButton")
    .addEventListener(
        "click",
        closeModal
    );


function closeModal() {

    modal.style.display = "none";

}


// ===============================
// CLOSE MODAL OUTSIDE
// ===============================

modal.addEventListener(
    "click",
    function (event) {

        if (event.target === modal) {

            closeModal();

        }

    }
);


// ===============================
// VEHICLE TYPE / DIMENSIONS
// ===============================

document
    .getElementById("newVehicleType")
    .addEventListener(
        "change",
        updateDimensionLimits
    );


function updateDimensionLimits() {

    const vehicleType =
        document
            .getElementById("newVehicleType")
            .value;


    const lengthInput =
        document
            .getElementById("newLength");


    const widthInput =
        document
            .getElementById("newWidth");


    const heightInput =
        document
            .getElementById("newHeight");


    const limitText =
        document
            .getElementById("dimensionLimitText");


    const lengthLimit =
        document
            .getElementById("lengthLimit");


    const widthLimit =
        document
            .getElementById("widthLimit");


    const heightLimit =
        document
            .getElementById("heightLimit");


    if (!legalLimits[vehicleType]) {

        lengthInput.max = "22";

        widthInput.max = "2.6";

        heightInput.max = "4.3";


        limitText.textContent =
            "Select a vehicle type to view the applicable limits.";


        lengthLimit.textContent =
            "Select vehicle type first.";


        widthLimit.textContent =
            "Maximum: 2.6 m";


        heightLimit.textContent =
            "Maximum: 4.3 m";


        return;

    }


    const limits =
        legalLimits[vehicleType];


    lengthInput.max =
        limits.length;


    widthInput.max =
        limits.width;


    heightInput.max =
        limits.height;


    limitText.textContent =
        `Maximum dimensions: ` +
        `${limits.length.toFixed(1)} m long × ` +
        `${limits.width.toFixed(1)} m wide × ` +
        `${limits.height.toFixed(1)} m high.`;


    lengthLimit.textContent =
        `Maximum: ${limits.length.toFixed(1)} m`;


    widthLimit.textContent =
        `Maximum: ${limits.width.toFixed(1)} m`;


    heightLimit.textContent =
        `Maximum: ${limits.height.toFixed(1)} m`;


    validateDimensions();

}


// ===============================
// DIMENSION VALIDATION
// ===============================

[
    "newLength",
    "newWidth",
    "newHeight"
].forEach(id => {

    document
        .getElementById(id)
        .addEventListener(
            "input",
            validateDimensions
        );

});


function validateDimensions() {

    const vehicleType =
        document
            .getElementById("newVehicleType")
            .value;


    if (!legalLimits[vehicleType]) {

        return false;

    }


    const limits =
        legalLimits[vehicleType];


    const length =
        Number(
            document
                .getElementById("newLength")
                .value
        );


    const width =
        Number(
            document
                .getElementById("newWidth")
                .value
        );


    const height =
        Number(
            document
                .getElementById("newHeight")
                .value
        );


    const lengthInput =
        document
            .getElementById("newLength");


    const widthInput =
        document
            .getElementById("newWidth");


    const heightInput =
        document
            .getElementById("newHeight");


    lengthInput.setCustomValidity(
        length > limits.length
            ? `Maximum length is ${limits.length} m.`
            : ""
    );


    widthInput.setCustomValidity(
        width > limits.width
            ? `Maximum width is ${limits.width} m.`
            : ""
    );


    heightInput.setCustomValidity(
        height > limits.height
            ? `Maximum height is ${limits.height} m.`
            : ""
    );


    return (
        length <= limits.length &&
        width <= limits.width &&
        height <= limits.height
    );

}


// ===============================
// SAVE PROFILE
// ===============================

document
    .getElementById("saveProfileButton")
    .addEventListener(
        "click",
        saveProfile
    );


async function saveProfile() {

    // ===============================
    // IDENTIFICATION
    // ===============================

    const vin =
        document
            .getElementById("newVin")
            .value
            .trim();


    const fleetNumber =
        document
            .getElementById("newFleetNumber")
            .value
            .trim();


    const name =
        document
            .getElementById("newTruckName")
            .value
            .trim();


    const registration =
        document
            .getElementById("newRegistration")
            .value
            .trim();


    const make =
        document
            .getElementById("newMake")
            .value
            .trim();


    const model =
        document
            .getElementById("newModel")
            .value
            .trim();


    const year =
        document
            .getElementById("newYear")
            .value;


    // ===============================
    // VEHICLE SPECIFICATIONS
    // ===============================

    const fuelType =
        document
            .getElementById("newFuelType")
            .value;


    const grossVehicleWeight =
        document
            .getElementById("newWeight")
            .value;


    const payloadCapacity =
        document
            .getElementById("newPayload")
            .value;


    const enginePower =
        document
            .getElementById("newEnginePower")
            .value;


    const fuelTankCapacity =
        document
            .getElementById("newFuel")
            .value;


    const axleCount =
        document
            .getElementById("newAxleCount")
            .value;


    const vehicleType =
        document
            .getElementById("newVehicleType")
            .value;


    // ===============================
    // DIMENSIONS
    // ===============================

    const length =
        document
            .getElementById("newLength")
            .value;


    const width =
        document
            .getElementById("newWidth")
            .value;


    const height =
        document
            .getElementById("newHeight")
            .value;


    // ===============================
    // OPERATION
    // ===============================

    const odometer =
        document
            .getElementById("newOdometer")
            .value;


    const status =
        document
            .getElementById("newStatus")
            .value;


    const lastServiceDate =
        document
            .getElementById("newLastService")
            .value;


    const nextServiceDue =
        document
            .getElementById("newNextService")
            .value;


    // ===============================
    // VALIDATION
    // ===============================

    if (
        !vin ||
        !fleetNumber ||
        !name ||
        !registration ||
        !make ||
        !model ||
        !year ||
        !fuelType ||
        !grossVehicleWeight ||
        !payloadCapacity ||
        !enginePower ||
        !fuelTankCapacity ||
        !axleCount ||
        !vehicleType ||
        !length ||
        !width ||
        !height ||
        !odometer
    ) {

        alert(
            "Please complete all required truck information."
        );

        return;

    }


    // ===============================
    // DIMENSION VALIDATION
    // ===============================

    if (!validateDimensions()) {

        alert(
            "The truck dimensions exceed the legal limits for the selected vehicle type."
        );

        return;

    }


    // ===============================
    // BUILD API PAYLOAD
    // ===============================

    const payload = {

        // Identification

        vin:
            vin,

        fleet_number:
            fleetNumber,

        name:
            name,

        registration:
            registration,

        make:
            make,

        model:
            model,

        year:
            Number(year),


        // Vehicle specifications

        fuel_type:
            fuelType,

        gross_vehicle_weight_kg:
            Number(grossVehicleWeight),

        payload_capacity_kg:
            Number(payloadCapacity),

        engine_power_kw:
            Number(enginePower),

        fuel_tank_capacity_l:
            Number(fuelTankCapacity),

        axle_count:
            Number(axleCount),


        // Vehicle type

        vehicle_type:
            vehicleType,


        // Dimensions

        length_m:
            Number(length),

        width_m:
            Number(width),

        height_m:
            Number(height),


        // Operation

        odometer_km:
            Number(odometer),

        status:
            status,

        last_service_date:
            lastServiceDate || null,

        next_service_due_km:
            nextServiceDue
                ? Number(nextServiceDue)
                : null

    };


    console.log(
        "Sending truck to API:",
        payload
    );


    // ===============================
    // SEND TO FASTAPI
    // ===============================

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/trucks/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(payload)
                }
            );


        // ===============================
        // API ERROR
        // ===============================

        if (!response.ok) {

            let errorMessage =
                "Failed to save truck profile.";


            try {

                const errorData =
                    await response.json();


                if (errorData.detail) {

                    if (
                        Array.isArray(
                            errorData.detail
                        )
                    ) {

                        errorMessage =
                            errorData.detail
                                .map(error =>
                                    error.msg
                                )
                                .join("\n");

                    }

                    else {

                        errorMessage =
                            errorData.detail;

                    }

                }

            }

            catch {

                // Response wasn't JSON

            }


            throw new Error(
                errorMessage
            );

        }


        // ===============================
        // GET SAVED TRUCK
        // ===============================

        const savedTruck =
            await response.json();


        // ===============================
        // STANDARDIZE PROFILE
        // ===============================

        const profile = {

            id:
                savedTruck.id,

            vin:
                savedTruck.vin ??
                vin,

            fleetNumber:
                savedTruck.fleet_number ??
                fleetNumber,

            name:
                savedTruck.name ??
                name,

            registration:
                savedTruck.registration ??
                registration,

            make:
                savedTruck.make ??
                make,

            model:
                savedTruck.model ??
                model,

            year:
                savedTruck.year ??
                Number(year),


            // Vehicle specifications

            fuelType:
                savedTruck.fuel_type ??
                fuelType,

            grossVehicleWeightKg:
                savedTruck.gross_vehicle_weight_kg ??
                Number(grossVehicleWeight),

            payloadCapacityKg:
                savedTruck.payload_capacity_kg ??
                Number(payloadCapacity),

            enginePowerKw:
                savedTruck.engine_power_kw ??
                Number(enginePower),

            fuelTankCapacityL:
                savedTruck.fuel_tank_capacity_l ??
                Number(fuelTankCapacity),

            axleCount:
                savedTruck.axle_count ??
                Number(axleCount),


            // Vehicle type

            vehicleType:
                savedTruck.vehicle_type ??
                vehicleType,


            // Dimensions

            lengthM:
                savedTruck.length_m ??
                Number(length),

            widthM:
                savedTruck.width_m ??
                Number(width),

            heightM:
                savedTruck.height_m ??
                Number(height),


            // Operation

            odometerKm:
                savedTruck.odometer_km ??
                Number(odometer),

            status:
                savedTruck.status ??
                status,

            lastServiceDate:
                savedTruck.last_service_date ??
                lastServiceDate ??
                null,

            nextServiceDueKm:
                savedTruck.next_service_due_km ??
                (
                    nextServiceDue
                        ? Number(nextServiceDue)
                        : null
                )

        };


        // ===============================
        // UPDATE LOCAL STATE
        // ===============================

        truckProfiles.push(
            profile
        );


        localStorage.setItem(
            "truckProfiles",
            JSON.stringify(
                truckProfiles
            )
        );


        // ===============================
        // UPDATE DROPDOWN
        // ===============================

        updateProfileDropdown();


        // ===============================
        // SELECT NEW TRUCK
        // ===============================

        document
            .getElementById("truckProfile")
            .value =
                profile.id;


        selectedProfile =
            profile;


        // ===============================
        // DISPLAY PROFILE
        // ===============================

        displayProfile(
            profile
        );


        // ===============================
        // CLOSE MODAL
        // ===============================

        closeModal();


        // ===============================
        // CLEAR FORM
        // ===============================

        clearProfileForm();


        console.log(
            "Truck profile saved successfully:",
            profile
        );

    }

    catch (err) {

        console.error(
            "Error saving truck:",
            err
        );


        alert(
            `Error: ${err.message}`
        );

    }

}


// ===============================
// CLEAR PROFILE FORM
// ===============================

function clearProfileForm() {

    const fields = [

        "newTruckName",
        "newFleetNumber",
        "newRegistration",
        "newVin",
        "newMake",
        "newModel",
        "newYear",
        "newWeight",
        "newPayload",
        "newEnginePower",
        "newFuel",
        "newAxleCount",
        "newLength",
        "newWidth",
        "newHeight",
        "newOdometer",
        "newLastService",
        "newNextService"

    ];


    fields.forEach(id => {

        const element =
            document.getElementById(id);


        if (element) {

            element.value = "";

        }

    });


    document
        .getElementById("newStatus")
        .value = "active";


    document
        .getElementById("newFuelType")
        .value = "";


    document
        .getElementById("newVehicleType")
        .value = "";


    document
        .getElementById("newAxleCount")
        .value = "2";


    document
        .getElementById("newVin")
        .setCustomValidity("");


    [
        "newLength",
        "newWidth",
        "newHeight"
    ].forEach(id => {

        document
            .getElementById(id)
            .setCustomValidity("");

    });


    updateDimensionLimits();

}


// ===============================
// ROUTE LAYER & CALCULATION
// ===============================

let routeLayerGroup = L.layerGroup().addTo(map);

document
    .getElementById("routeButton")
    .addEventListener("click", calculateRoute);

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
            fleet_number: selectedProfile.fleetNumber,
            registration: selectedProfile.registration,
            gross_vehicle_weight_kg: selectedProfile.grossVehicleWeightKg,
            fuel_tank_capacity_l: selectedProfile.fuelTankCapacityL,
            vehicle_type: selectedProfile.vehicleType,
            length_m: selectedProfile.lengthM,
            width_m: selectedProfile.widthM,
            height_m: selectedProfile.heightM
        },
        driver: {
            name: driverName || "Unassigned",
            licence: document.getElementById("driverLicence").value,
            phone: document.getElementById("driverPhone").value,
            driving_hours: Number(document.getElementById("driverHours").value) || 9.0
        }
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/route", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(routeRequest)
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const routeData = await response.json();

        // Update Information Panels
        if (document.getElementById("distance")) {
            document.getElementById("distance").textContent = `${routeData.distance_km} km`;
        }
        if (document.getElementById("duration")) {
            document.getElementById("duration").textContent = routeData.duration_text;
        }
        if (document.getElementById("fuelRequired")) {
            document.getElementById("fuelRequired").textContent = `${routeData.fuel_required_liters} L`;
        }

        // Draw Route on the Map
        drawRoute(routeData);

    } catch (err) {
        console.error("Error calculating route:", err);
        alert("Failed to calculate route. Make sure your FastAPI backend is running and the /route endpoint exists.");
    }
}

function drawRoute(route) {
    routeLayerGroup.clearLayers();

    // Markers for start and destination
    const startMarker = L.marker(route.start_coord).bindPopup(`<b>Start:</b> Origin`);
    const destMarker = L.marker(route.dest_coord).bindPopup(`<b>Destination:</b> Destination`);
    
    // Draw route polyline
    const polyline = L.polyline(route.waypoints, {
        color: "#2563eb",
        weight: 6,
        opacity: 0.85
    });

    routeLayerGroup.addLayer(startMarker);
    routeLayerGroup.addLayer(destMarker);
    routeLayerGroup.addLayer(polyline);

    // Zoom map to fit the route
    map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
}


// ===============================
// START APPLICATION
// ===============================

loadProfiles();