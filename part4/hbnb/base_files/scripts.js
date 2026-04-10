document.addEventListener("DOMContentLoaded", () => {
    setupLogin();
    checkAuthentication();
    setupPriceFilter();

    const placeDetailsContainer = document.getElementById("place-details");
    if (placeDetailsContainer) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }

    setupReviewForm();
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

        if (!email || !password) {
            alert("Email and password are required");
            return;
        }

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
    // Make a GET request to fetch places data
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
            method: "GET",
            headers: {
                // Include the token in the Authorization header
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        // Handle the response and pass the data to displayPlaces function
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
    const addReviewLink = document.getElementById('add-review');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewLink) {
            addReviewLink.style.display = 'none';
        }
    } else {
        if (loginLink) loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }

    return token;
}

// Fetch the cookie from the identified user
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

    // Clear the current content of the places list
    placesList.innerHTML = "";

    // Iterate over the places data
    places.forEach(place => {
        const div = document.createElement("div");
        div.classList.add("place-card");

        // For each place, create a div element and set its content
        div.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        // Append the created element to the places list
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

    // Get the selected price value
    priceFilter.innerHTML = `
        <option value="">All</option>
        <option value="10">$10</option>
        <option value="50">$50</option>
        <option value="100">$100</option>
    `;

    // Iterate over the places and show/hide them based on the selected price
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

// Fecth the details of a place from the python code
async function fetchPlaceDetails(token, placeId) {
    try {
        // Make a GET request to fetch place details
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: "GET",
            headers: {
                // Include the token in the Authorization header
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        const placeDetails = document.getElementById("place-details");

        // Handle the response and pass the data to displayPlaceDetails function
        if (!data) {
            placeDetails.innerHTML = "<p>Place not found.</p>";
            return;
}
        displayPlaceDetails(data);

    } catch (error) {
        console.error("Error:", error);
    }
}

// Function used to display all the info about a place
function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    const placeDetails = document.getElementById("place-details");
    if (!place || !placeDetails) {
    if (placeDetails) placeDetails.innerHTML = "<p>Place not found.</p>";
    return;
}

    if (!placeDetails) return;

    const addReviewLink = document.getElementById("add-review-link");
    if (addReviewLink) {
        addReviewLink.href = `add_review.html?id=${place.id}`;
    }

    // Create elements to display the place details (name, description, price, amenities and reviews)

    let amenities = "None";
    if (Array.isArray(place.amenities) && place.amenities.length > 0) {
        amenities = place.amenities.map(a => a.name).join(', ');
    }

    placeDetails.innerHTML = `
        <div class ="place-details">
            <h1>${place.title}</h1>
            <p><strong> Host: </strong> ${place.owner}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <p><strong>Description:</strong>${place.description}</p>
            <p><strong>Amenities:</strong> ${amenities}</p>
        </div>
    `;
    displayReviews(place);
}

// Function used to submit the review that a user write
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: rating,
                place_id: placeId
            })
        });

        handleResponse(response, token, placeId);

    } catch (error) {
        console.error("Error submitting review:", error);
        alert("Network or server error");
    }
}

async function handleResponse(response, token, placeId) {
    const data = await response.json().catch(() => null);

    if (response.ok) {
        alert("Review submitted successfully!");

        document.getElementById("review-form").reset();

        // refresh page data
        fetchPlaceDetails(token, placeId);

    } else {
        const errorMessage =
            data?.error ||
            data?.message ||
            data?.detail ||
            "Unknown error";

        alert("Error: " + errorMessage);
    }
}

function setupReviewForm() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        if (!token) {
            alert("You must be logged in to submit a review.");
            return;
        }

        const reviewText = document.getElementById('review').value;
        const rating = parseInt(document.getElementById('rating').value);

        if (!reviewText || reviewText.trim() === "") {
            alert("Review cannot be empty");
            return;
        }

        if (isNaN(rating) || rating < 1 || rating > 5) {
            alert("Rating must be between 1 and 5");
            return;
        }

        submitReview(token, placeId, reviewText, rating);
    });
}

// Display reviews inside of the place details
function displayReviews(place) {
    const reviewsContainer = document.getElementById("reviews");
    if (!reviewsContainer) return;

    let reviewsHTML = "<p>No reviews yet.</p>";

    if (place.reviews && place.reviews.length > 0) {
        reviewsHTML = place.reviews.map(r => `
            <div class="review-card">
                <p><strong>User:</strong> ${r.user.first_name} ${r.user.last_name}</p>
                <p>Rating: ${"⭐".repeat(r.rating)}</p>
                <p>${r.text}</p>
            </div>
        `).join('');
    }

    reviewsContainer.innerHTML = `
        <h3>Reviews</h3>
        ${reviewsHTML}
    `;
}