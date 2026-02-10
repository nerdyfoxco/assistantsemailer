import requests

def get_token():
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "username": "admin@example.com",
        "password": "password123"
    }
    try:
        # Auth endpoint expects JSON with email/password (LoginRequest)
        response = requests.post(url, json={"email": "admin@example.com", "password": "password123"})
        if response.status_code == 200:
            token = response.json().get("access_token")
            # Write token to a file so PowerShell can read it
            with open("face/token.txt", "w") as f:
                f.write(token)
            print(f"Token retrieved successfully.")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")

if __name__ == "__main__":
    get_token()
