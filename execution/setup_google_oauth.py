"""
Script: setup_google_oauth.py
Purpose: One-time OAuth setup for Google Sheets access using your personal Google account
Inputs: None (interactive browser flow)
Outputs: token.json with OAuth credentials
Author: AI-Assisted
Created: 2025-11-30

This uses OAuth 2.0 "installed application" flow - much simpler than service accounts.
You authenticate once, and the token is saved for future use.
"""

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle

# Scopes required for Google Sheets access
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

def setup_oauth():
    """
    Set up OAuth 2.0 authentication using installed application flow
    """
    print("\n" + "="*80)
    print("GOOGLE OAUTH SETUP - Personal Account Authentication")
    print("="*80)

    creds = None
    token_file = 'token.pickle'

    # Check if we already have valid credentials
    if os.path.exists(token_file):
        print("\n[INFO] Found existing token file")
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[INFO] Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("\n[INFO] Starting OAuth flow...")

            # Check for credentials file first
            if not os.path.exists('oauth_credentials.json'):
                print("\n[ERROR] oauth_credentials.json not found!")
                print("\nYou'll need client credentials from Google Cloud Console.")
                print("Don't worry - this is much simpler than service accounts!")
                print("\nQuick setup:")
                print("1. Go to: https://console.cloud.google.com/apis/credentials")
                print("2. Click 'Create Credentials' > 'OAuth client ID'")
                print("3. Application type: 'Desktop app'")
                print("4. Download the JSON file")
                print("5. Save it as 'oauth_credentials.json' in this workspace folder:")
                print(f"   {os.path.abspath('oauth_credentials.json')}")
                print("\nOnce you have the file, run this script again.")
                return False

            # Run OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                'oauth_credentials.json',
                SCOPES
            )

            print("\n[INFO] Opening browser for authentication...")
            print("Please log in with your Google account and grant permissions.")

            creds = flow.run_local_server(port=0)

            print("\n[OK] Authentication successful!")

        # Save credentials for next time
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

        print(f"[OK] Credentials saved to {token_file}")
    else:
        print("[OK] Valid credentials already exist")

    print("\n" + "="*80)
    print("SETUP COMPLETE")
    print("="*80)
    print("\nYou can now run the automated scraper with Google Sheets integration:")
    print("  python execution/scrape_therapists_automated.py")
    print("\n" + "="*80)

    return True

def main():
    success = setup_oauth()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
