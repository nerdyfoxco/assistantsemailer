import requests
from spine.core.config import settings

def verify_creds():
    print(f"Checking Credentials for Client ID: {settings.GOOGLE_CLIENT_ID[:15]}...")
    
    # We attempt to exchange a dummy code.
    # Google will validate the Client ID/Secret BEFORE checking the code.
    # If Creds are WRONG -> "invalid_client"
    # If Creds are RIGHT but Code is BAD -> "invalid_grant"
    
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": "fake_code_to_test_creds",
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI
    }
    
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        error = data.get("error")
        
        print(f"Status: {response.status_code}")
        print(f"Error Code: {error}")
        print(f"Full Response: {data}")
        
        if error == "invalid_client":
            print("\n[FAIL] Credentials are INVALID.")
        elif error == "invalid_grant":
            print("\n[SUCCESS] Credentials are VALID (Server accepted Client ID/Secret).")
        elif error == "redirect_uri_mismatch":
             print("\n[SUCCESS] Credentials are VALID, but Redirect URI mismatch (expected behavior for dummy code, but confirms Client ID is known).")
        else:
             print(f"\n[?] Unknown State: {error}")
             
    except Exception as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":
    verify_creds()
