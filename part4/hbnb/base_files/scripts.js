document.addEventListener("DOMContentLoaded", () => {
    fetchPlaces();
    setupPriceFilter();
    setupLogin();
});

let allPlaces = [];

// Fetch the places from the Python code
function fetchPlaces() {
    fetch("http://127.0.0.1:5000/api/v1/places")
        .then(response => response.json())
        .then(data => {
            allPlaces = data;
            displayPlaces(data);
            populatePriceFilter(data);
        })
        .catch(error => console.error("Error:", error));
}

// Show all the places created in the database
function displayPlaces(places) {
    const placesList = document.getElementById("places-list");

    if (!placesList) return; // stop if element doesn't exist

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

// Fetch the prices of all the places
function populatePriceFilter(places) {
    const priceFilter = document.getElementById("price-filter");
    if (!priceFilter) return;

    priceFilter.innerHTML = `<option value="">All</option>`;

    const prices = [...new Set(places.map(p => p.price))].sort((a, b) => a - b);

    prices.forEach(price => {
        const option = document.createElement("option");
        option.value = price;
        option.textContent = `$${price}`;
        priceFilter.appendChild(option);
    });
}

// Order the places with the max price we want
function setupPriceFilter() {
    const priceFilter = document.getElementById("price-filter");
    if (!priceFilter) return;
    priceFilter.addEventListener("change", () => {
        const maxPrice = priceFilter.value ? parseFloat(priceFilter.value) : null;

        let filteredPlaces = allPlaces;

        if (maxPrice !== null) {
            filteredPlaces = allPlaces.filter(place => place.price <= maxPrice);
        }

        displayPlaces(filteredPlaces);
    });
}

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