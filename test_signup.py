import requests
import uuid

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_signup():
    unique_name = f"User {uuid.uuid4().hex[:8]}"
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"

    print(f"Testing SIGNUP with {unique_email}...")
    
    payload = {
        "email": unique_email,
        "password": password,
        "name": unique_name
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"SUCCESS: Got token {token[:10]}...")
            
            # Save token for screenshot script
            with open("face/token.txt", "w") as f:
                f.write(token)
            
            # Verify access
            headers = {"Authorization": f"Bearer {token}"}
            work_items = requests.get(f"{BASE_URL}/work-items/", headers=headers)
            print(f"Work Items Access: {work_items.status_code}")
        else:
            print("FAILED to signup.")

    except Exception as e:
        print(f"Signup Request failed: {e}")

if __name__ == "__main__":
    test_signup()
