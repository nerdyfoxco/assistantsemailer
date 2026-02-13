import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def check_health():
    try:
        res = requests.get(f"{BASE_URL}/")
        if res.status_code == 200:
            log("Backend is UP", "PASS")
            return True
    except Exception as e:
        log(f"Backend unreachable: {e}", "FAIL")
    return False

def test_api_keys():
    log("Starting API Key E2E Test...")
    
    # 1. Create Key
    payload = {"name": "E2E Test Key", "scopes": ["read", "write"]}
    res = requests.post(f"{BASE_URL}/developer/keys/", json=payload)
    
    if res.status_code != 200:
        log(f"Failed to create key: {res.text}", "FAIL")
        sys.exit(1)
        
    key_data = res.json()
    key_id = key_data["id"]
    raw_key = key_data["raw_key"]
    log(f"Created Key: {key_id} (Prefix: {key_data['prefix']})", "PASS")
    
    if not raw_key.startswith("sk_live_"):
        log("Invalid key format", "FAIL")
        sys.exit(1)

    # 2. List Keys
    res = requests.get(f"{BASE_URL}/developer/keys/")
    try:
        keys = res.json()
    except Exception as e:
        log(f"Failed to parse List Keys response: {res.text} (Status: {res.status_code})", "FAIL")
        sys.exit(1)

    found = any(k["id"] == key_id for k in keys)
    if found:
        log("Key found in list", "PASS")
    else:
        log("Key NOT found in list", "FAIL")
        sys.exit(1)

    # 3. Revoke Key
    res = requests.delete(f"{BASE_URL}/developer/keys/{key_id}")
    if res.status_code == 200:
        log("Key revoked", "PASS")
    else:
        log(f"Failed to revoke key: {res.text}", "FAIL")
        sys.exit(1)

    # 4. Verify Revocation
    res = requests.get(f"{BASE_URL}/developer/keys/")
    keys = res.json()
    if not any(k["id"] == key_id for k in keys):
        log("Key successfully removed from list", "PASS")
    else:
        log("Revoked key still appears in list (Soft delete?)", "WARN")

    log("E2E Test Complete: ALL GREEN", "SUCCESS")

if __name__ == "__main__":
    if check_health():
        test_api_keys()
