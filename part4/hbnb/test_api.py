import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

# ----------------- Fonctions existantes -----------------
def create_user(first_name, last_name, email, password):
    resp = requests.post(
        f"{BASE_URL}/users/",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
    )
    print(f"Create user {email}: {resp.status_code}, {resp.text}")
    return resp.json() if resp.status_code == 201 else None

def login_user(email, password):
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    print(f"Login {email}: {resp.status_code}, {resp.text}")
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None

def create_place(token, title, price, latitude, longitude, owner_id):
    resp = requests.post(
        f"{BASE_URL}/places/",
        json={
            "title": title,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "owner_id": owner_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Create place: {resp.status_code}, {resp.text}")
    return resp.json() if resp.status_code == 201 else None

def update_place(token, place_id, title, price, latitude, longitude):
    resp = requests.put(
        f"{BASE_URL}/places/{place_id}",
        json={
            "title": title,
            "price": price,
            "latitude": latitude,
            "longitude": longitude
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Update place {place_id}: {resp.status_code}, {resp.text}")
    return resp.json() if resp.status_code == 200 else None

def create_review(token, place_id, text, rating):
    resp = requests.post(
        f"{BASE_URL}/reviews/",
        json={
            "place_id": place_id,
            "text": text,
            "rating": rating
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Create review: {resp.status_code}, {resp.text}")
    return resp.json() if resp.status_code == 201 else None

# ----------------- Nouveaux tests -----------------

def delete_review(token, review_id):
    """Test de suppression d'une review"""
    resp = requests.delete(
        f"{BASE_URL}/reviews/{review_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Delete review {review_id}: {resp.status_code}, {resp.text}")
    return resp.status_code == 204  # 204 No Content = succès

def update_user(token, user_id, first_name=None, last_name=None, email=None):
    """Test de mise à jour d'un utilisateur"""
    data = {}
    if first_name:
        data["first_name"] = first_name
    if last_name:
        data["last_name"] = last_name
    if email:
        data["email"] = email

    resp = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    print(f"Update user {user_id}: {resp.status_code}, {resp.text}")
    return resp.json() if resp.status_code == 200 else None

def get_reviews(token):
    """Test de lecture des reviews (vérification simple)"""
    resp = requests.get(
        f"{BASE_URL}/reviews/",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Get reviews: {resp.status_code}, {resp.text}")
    return resp.json() if resp.status_code == 200 else None

# ----------------- Script principal -----------------
def main():
    # Créer deux utilisateurs
    user1 = create_user("John", "Doe", "john.doe@example.com", "string")
    user2 = create_user("Johnn", "Doee", "johnn.doee@example.com", "string")

    # Connexion
    token1 = login_user("john.doe@example.com", "string")
    token2 = login_user("johnn.doee@example.com", "string")

    # Créer une place avec le premier utilisateur
    place = create_place(token1, "New Place", 0, 0.0, 0.0, user1["id"])
    place_id = place.get("id")

    # Création d’une review par le second utilisateur
    review = create_review(token2, place_id, "Great place!", 4)
    review_id = review.get("id")

    # -------- Tests supplémentaires --------
    # 1️⃣ Suppression de la review
    delete_review(token2, review_id)

    # 2️⃣ Mise à jour du premier utilisateur
    update_user(token1, user1["id"], first_name="John Updated")

    # 3️⃣ Lecture des reviews pour vérifier qu'il n'y a plus de review
    get_reviews(token2)

if __name__ == "__main__":
    main()
