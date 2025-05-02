import json
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the required scope for DV360 (DoubleClick Bid Manager)
SCOPES = ['https://www.googleapis.com/auth/doubleclickbidmanager']

def get_service():
    # Load credentials from Streamlit secrets
    service_account_info = json.loads(st.secrets["SERVICE_ACCOUNT_JSON"])
    
    # Create credentials object
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    
    # Build and return the DV360 API client
    service = build('doubleclickbidmanager', 'v1.1', credentials=creds)
    return service