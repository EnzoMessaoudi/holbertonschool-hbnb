document.addEventListener("DOMContentLoaded", () => {
    setupLogin();
    checkAuthentication();
    setupPriceFilter();

    // Detect if we are on place.html and load details
    const placeDetailsContainer = document.getElementById("place-details");
    if (placeDetailsContainer) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token'); // can be null if not logged in
        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }
});

let allPlaces = [];

// Function used to log in a user
function setupLogin() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = 'index.html';
                alert('Welcome !');
            } else {
                const errorData = await response.json();
                alert('Login failed: ' + (errorData.message || response.statusText));
            }

        } catch (error) {
            console.error('Login request failed', error);
            alert('An error occurred while logging in.');
        }
    });
}

// Fetch the places from the Python code
async function fetchPlaces(token) {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        allPlaces = data;
        displayPlaces(data);

    } catch (error) {
        console.error("Error:", error);
    }
}

// Function that check if a user is connected or no (Used in Index and place details)
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        fetchPlaces()
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');

        if (key === name) {
            return value;
        }
    }

    return null;
}

// Show all the places created in the database
function displayPlaces(places, selectedPrice) {
    const placesList = document.getElementById("places-list");

    if (!placesList) return;

    placesList.innerHTML = "";

    places.forEach(place => {
        const div = document.createElement("div");
        div.classList.add("place-card");

        div.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;

        placesList.appendChild(div);

        const button = div.querySelector(".details-button");
        button.addEventListener("click", () => {
            window.location.href = `place.html?id=${place.id}`;
        });
    });
}

// Order the places with the max price we want
function setupPriceFilter() {
    const priceFilter = document.getElementById("price-filter");
    if (!priceFilter) return;

    priceFilter.innerHTML = `
        <option value="">All</option>
        <option value="10">$10</option>
        <option value="50">$50</option>
        <option value="100">$100</option>
    `;

    priceFilter.addEventListener("change", () => {
        const maxPrice = priceFilter.value ? parseFloat(priceFilter.value) : null;
        const filteredPlaces = maxPrice
            ? allPlaces.filter(place => place.price <= maxPrice)
            : allPlaces;
        displayPlaces(filteredPlaces);
    });
}

//Get the ID of the place from the URL
function getPlaceIdFromURL() {
    let params = new URLSearchParams(location.search);
    const id = params.get('id');
    return id;
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();

        if (!data) {
            placeDetails.innerHTML = "<p>Place not found.</p>";
            return;
}

        displayPlaceDetails(data);

    } catch (error) {
        console.error("Error:", error);
    }
}

function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    const placeDetails = document.getElementById("place-details");
    if (!place || !placeDetails) {
    if (placeDetails) placeDetails.innerHTML = "<p>Place not found.</p>";
    return;
}

    if (!placeDetails) return;

    // Create elements to display the place details (name, description, price, amenities and reviews)

    let amenities = "None";
    if (Array.isArray(place.amenities) && place.amenities.length > 0) {
        amenities = place.amenities.map(a => a.name).join(', ');
    }

    let reviewsHTML = "No reviews yet.";
    if (place.reviews && place.reviews.length > 0) {
        reviewsHTML = place.reviews.map(r => `<p><strong>${r.user}:</strong> ${r.text}</p>`).join('');
    }

    placeDetails.innerHTML = `
        <div class ="place-details">
            <h2>${place.title}</h2>
            <p>${place.description}</p>
            <p>Price per night: $${place.price}</p>
            <p>Amenities: ${amenities}</p>
            <p>reviews: ${reviewsHTML}</p>
        </div>
    `;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewLink = document.getElementById('add-review');

    if (!token) {
        if (loginLink)
        loginLink.style.display = 'block';
        fetchPlaces()
        addReviewLink.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}