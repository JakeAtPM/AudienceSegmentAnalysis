import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

credentials = service_account.Credentials.from_service_account_info(
    st.secrets['BIGQUERY_CREDS_JSON']
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)


### TO-DO
# Look into permanent table joins (sql views rather than a whole new table???) so that we can query zipcode at the same time as other PII
# Refined query to get exactly what we need without the need for much additional formatting
# Work on interaction between custom_match_upload.py, app.py, and this file