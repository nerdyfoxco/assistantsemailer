import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found.")
                print("Please download your OAuth Client ID JSON from Google Cloud Console.")
                print("Save it as 'credentials.json' in this directory.")
                return None

            # Try to load either web or installed app config
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            except ValueError:
                 # Fallback for 'web' format if the lib complains, but usually it parses both.
                 # The issue is run_local_server vs redirect_uri matches.
                 pass

            # IMPORTANT: Port 8000 MUST be used because the Redirect URI is registered as ...:8000
            # open_browser=False to allow Agent to see the URL in stdout
            creds = flow.run_local_server(port=8000, open_browser=False)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

if __name__ == '__main__':
    print(">>> Starting Gmail Authentication Flow...")
    creds = authenticate_gmail()
    if creds:
        print(">>> Authentication Successful. 'token.json' created.")
        print(f"    Token: {creds.token[:10]}...")
