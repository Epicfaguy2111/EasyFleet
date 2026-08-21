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
// LOAD PROFILES
// ===============================

function loadProfiles() {

    const savedProfiles =
        localStorage.getItem("truckProfiles");

    if (savedProfiles) {

        truckProfiles =
            JSON.parse(savedProfiles);

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

        option.value = profile.id;

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


            displayProfile(
                selectedProfile
            );
        }
    );


// ===============================
// DISPLAY PROFILE
// ===============================

function displayProfile(profile) {

    document
        .getElementById("truckInfoPanel")
        .style.display = "block";


    document
        .getElementById("truckName")
        .textContent = profile.name;


    document
        .getElementById("registration")
        .textContent = profile.registration;


    document
        .getElementById("truckWeight")
        .textContent =
            `${profile.weight} tons`;


    document
        .getElementById("truckHeight")
        .textContent =
            `${profile.height} m`;


    document
        .getElementById("truckLength")
        .textContent =
            `${profile.length} m`;


    document
        .getElementById("truckFuel")
        .textContent =
            `${profile.fuel} L`;


    // Load default driver

    document
        .getElementById("driverName")
        .value =
            profile.driver.name;


    document
        .getElementById("driverLicence")
        .value =
            profile.driver.licence;


    document
        .getElementById("driverPhone")
        .value =
            profile.driver.phone;
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
// SAVE PROFILE
// ===============================

document
    .getElementById("saveProfileButton")
    .addEventListener(
        "click",
        saveProfile
    );


function saveProfile() {

    const name =
        document
            .getElementById("newTruckName")
            .value.trim();


    const registration =
        document
            .getElementById("newRegistration")
            .value.trim();


    const weight =
        document
            .getElementById("newWeight")
            .value;


    const height =
        document
            .getElementById("newHeight")
            .value;


    const length =
        document
            .getElementById("newLength")
            .value;


    const fuel =
        document
            .getElementById("newFuel")
            .value;


    const driverName =
        document
            .getElementById("newDriverName")
            .value.trim();


    const driverLicence =
        document
            .getElementById("newDriverLicence")
            .value.trim();


    const driverPhone =
        document
            .getElementById("newDriverPhone")
            .value.trim();


    // Basic validation

    if (
        !name ||
        !registration ||
        !weight ||
        !height ||
        !length ||
        !fuel
    ) {

        alert(
            "Please complete all truck information."
        );

        return;
    }


    const profile = {

        id: Date.now(),

        name: name,

        registration: registration,

        weight: Number(weight),

        height: Number(height),

        length: Number(length),

        fuel: Number(fuel),

        driver: {

            name: driverName,

            licence: driverLicence,

            phone: driverPhone

        }
    };


    truckProfiles.push(profile);


    localStorage.setItem(
        "truckProfiles",
        JSON.stringify(truckProfiles)
    );


    updateProfileDropdown();


    // Automatically select new profile

    document
        .getElementById("truckProfile")
        .value = profile.id;


    selectedProfile = profile;

    displayProfile(profile);


    closeModal();


    clearProfileForm();
}


// ===============================
// CLEAR PROFILE FORM
// ===============================

function clearProfileForm() {

    document
        .getElementById("newTruckName")
        .value = "";


    document
        .getElementById("newRegistration")
        .value = "";


    document
        .getElementById("newWeight")
        .value = "";


    document
        .getElementById("newHeight")
        .value = "";


    document
        .getElementById("newLength")
        .value = "";


    document
        .getElementById("newFuel")
        .value = "";


    document
        .getElementById("newDriverName")
        .value = "";


    document
        .getElementById("newDriverLicence")
        .value = "";


    document
        .getElementById("newDriverPhone")
        .value = "";
}


// ===============================
// CALCULATE ROUTE
// ===============================

document
    .getElementById("routeButton")
    .addEventListener(
        "click",
        calculateRoute
    );


async function calculateRoute() {

    const start =
        document
            .getElementById("start")
            .value;


    const destination =
        document
            .getElementById("destination")
            .value;


    const driverName =
        document
            .getElementById("driverName")
            .value;


    if (!selectedProfile) {

        alert(
            "Please select a truck profile."
        );

        return;
    }


    if (!start || !destination) {

        alert(
            "Please enter a starting location and destination."
        );

        return;
    }


    const routeRequest = {

        start: start,

        destination: destination,

        truck: {

            name: selectedProfile.name,

            registration:
                selectedProfile.registration,

            weight:
                selectedProfile.weight,

            height:
                selectedProfile.height,

            length:
                selectedProfile.length,

            fuel:
                selectedProfile.fuel
        },

        driver: {

            name: driverName,

            licence:
                document
                    .getElementById("driverLicence")
                    .value,

            phone:
                document
                    .getElementById("driverPhone")
                    .value,

            drivingHours:
                document
                    .getElementById("driverHours")
                    .value
        }
    };


    console.log(
        "Sending to FastAPI:",
        routeRequest
    );


    /*
        NEXT STEP:

        const response = await fetch(
            "http://127.0.0.1:8000/route",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(routeRequest)
            }
        );

        const route =
            await response.json();

        drawRoute(route);
    */
}


// ===============================
// START APPLICATION
// ===============================

loadProfiles();