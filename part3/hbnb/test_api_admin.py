import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"


def register_classic_user(email, first_name, last_name, password):
    """Créer un utilisateur classique via /register"""
    resp = requests.post(
        f"{BASE_URL}/users/register",
        json={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        }
    )
    print("Register classic user:", resp.status_code)
    print(resp.text)
    if resp.status_code == 201:
        return resp.json()
    return None


def login_user(email, password):
    """Login utilisateur pour récupérer le token JWT"""
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    print("Login user:", resp.status_code)
    print(resp.text)
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None


def create_user_admin(token, email, first_name, last_name, password):
    """Créer un utilisateur via le token admin"""
    resp = requests.post(
        f"{BASE_URL}/users/",
        json={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print("Create user via admin token:", resp.status_code)
    print(resp.text)
    if resp.status_code == 201:
        return resp.json()
    return None


def main():
    # 1️⃣ Créer un utilisateur classique
    classic_user = register_classic_user(
        "classicuser@example.com",
        "Classic",
        "User",
        "password123"
    )
    if not classic_user:
        print("Failed to create classic user")
        return

    # 2️⃣ Login du super admin (créé automatiquement dans create_app)
    admin_token = login_user("admin@example.com", "adminpassword")
    if not admin_token:
        print("Admin login failed")
        return
    print("Admin token:", admin_token)

    # 3️⃣ Créer un autre utilisateur via token admin
    admin_created_user = create_user_admin(
        admin_token,
        "seconduser@example.com",
        "Second",
        "User",
        "password123"
    )
    if admin_created_user:
        print("Successfully created user via admin route:", admin_created_user)
    else:
        print("Failed to create user via admin route")


if __name__ == "__main__":
    main()