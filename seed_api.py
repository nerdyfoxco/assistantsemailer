import requests
import sys

def seed_via_api():
    url = "http://localhost:8000/api/v1/users/"
    payload = {
        "email": "admin@example.com",
        "password": "password123",
        "full_name": "Admin User"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            print("User created successfully.")
        elif response.status_code == 400:
            print("User likely already exists.")
        else:
            print(f"Failed to create user: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"API Request failed: {e}")

if __name__ == "__main__":
    seed_via_api()
