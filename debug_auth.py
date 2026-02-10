import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_login(email, password):
    print(f"\n--- Testing Login for {email} ---")
    
    # 1. Try JSON with 'email'
    try:
        payload = {"email": email, "password": password}
        resp = requests.post(f"{BASE_URL}/auth/login", json=payload)
        print(f"JSON (email): {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"JSON (email) Error: {e}")

    # 2. Try JSON with 'username'
    try:
        payload = {"username": email, "password": password}
        resp = requests.post(f"{BASE_URL}/auth/login", json=payload)
        print(f"JSON (username): {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"JSON (username) Error: {e}")

    # 3. Try Form Data (OAuth2 standard)
    try:
        data = {"username": email, "password": password}
        resp = requests.post(f"{BASE_URL}/auth/login", data=data)
        print(f"Form Data: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Form Data Error: {e}")

if __name__ == "__main__":
    test_login("ashim.khanna.cv@gmail.com", "password123")
    test_login("admin@example.com", "admin")
