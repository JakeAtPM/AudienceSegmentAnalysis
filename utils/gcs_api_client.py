import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

# === Set OAuth scopes and redirect URI ===
SCOPES = ["https://www.googleapis.com/auth/doubleclickbidmanager"]
REDIRECT_URI = "http://localhost:8080"

# === Check if we already have valid credentials ===
TOKEN_PATH = "token.pickle"

def load_credentials():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token_file:
            return pickle.load(token_file)
    return None

def save_credentials(creds):
    with open(TOKEN_PATH, "wb") as token_file:
        pickle.dump(creds, token_file)


def authenticate_user_oauth():
    client_config = {
        "installed": {
            'client_id': st.secrets[OAUTH_CLIENT_ID],
            'client_secret': st.secrets[OAUTH_CLIENT_SECRET],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri = REDIRECT_URI
    )

    auth_url, _ = flow.authorization_url(prompt='consent')

    print("\n👉 Visit this URL to authorize access:")
    print(auth_url)
    print("\nThen paste the authorization code below.\n")

    code = input("Enter authorization code: ").strip()
    flow.fetch_token(code=code)
    creds = flow.credentials
    save_credentials(creds)
    return creds

def main():
    creds = load_credentials()
    if not creds:
        creds = authenticate_user_oauth()

    service = build('doubleclickbidmanager', 'v2', credentials=creds)

    print("\nConnected to Display & Video 360 API.\n")

    try:
        response = service.queries().list().execute()
        queries = response.get('queries', [])

        if not queries:
            print("No saved queries found.")
        else:
            print("Saved Queries:")
            for q in queries:
                print(f" - {q['metadata']['title']} (ID: {q['queryId']})")

    except Exception as e:
        print("Error accessing DV360 API:", e)

if __name__ == "__main__":
    main()