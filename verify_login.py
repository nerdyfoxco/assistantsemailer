import requests
import sys

def verify_login():
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "email": "agent_retry_2@example.com",
        "password": "password123"
    }
    try:
        print(f"Testing POST {url} with JSON payload...")
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200 and "access_token" in response.json():
            print("SUCCESS: Login successful and token received.")
            sys.exit(0)
        else:
            print("FAILURE: Login failed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_login()
