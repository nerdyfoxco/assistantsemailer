import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
DOCS_URL = "http://127.0.0.1:8000/docs"

def test_work_items():
    print(f"Testing GET {DOCS_URL} ...")
    try:
        r = requests.get(DOCS_URL)
        print(f"Docs Status: {r.status_code}")
    except Exception as e:
        print(f"Docs failed: {e}")

    try:
        with open("face/token.txt", "r") as f:
            token = f.read().strip()
    except FileNotFoundError:
        print("Token file not found. Run get_token.py first.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"Testing GET {BASE_URL}/work-items/ with token...")
    try:
        response = requests.get(f"{BASE_URL}/work-items/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

    print(f"Testing OPTIONS {BASE_URL}/work-items/ ...")
    try:
        opt_headers = {
            "Origin": "http://localhost:3006",
            "Access-Control-Request-Method": "GET"
        }
        res = requests.options(f"{BASE_URL}/work-items/", headers=opt_headers)
        print(f"OPTIONS Status: {res.status_code}")
        print(f"OPTIONS Headers: {res.headers}")
    except Exception as e:
        print(f"OPTIONS failed: {e}")

if __name__ == "__main__":
    test_work_items()
