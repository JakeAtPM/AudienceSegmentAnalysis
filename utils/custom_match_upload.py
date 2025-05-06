import hashlib
import base64
import pandas as pd
import phonenumbers
import json

def hash_pii(value:str) -> str:
    if not value or pd.isna(value):
        return ""
    normalized = str(value).strip().lower().encode()
    return base64.b64encode(hashlib.sha256(normalized).digest()).decode()


def format_e164(series: pd.Series, region: str = "US") -> pd.Series:
    def _format(phone):
        try:
            parsed = phonenumbers.parse(str(phone), region)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except:
            return ""
        return ""
    return series.fillna("").map(_format)


def prepare_customer_match (df: pd.DataFrame) -> dict:
    required_columns = {'email', 'firstName', 'lastName', 'phone'}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    
    df = df.copy()
    
    df['phone'] = format_e164(df['phone'])
    df['hashedEmail'] = df['email'].map(hash_pii)
    df['hashedFirstName'] = df['firstName'].map(hash_pii)
    df['hashedLastName'] = df['lastName'].map(hash_pii)
    df['hashedPhoneNumber'] = df['phone'].map(hash_pii)
    
    contact_info_list = df[[
        'hashedEmail', 'hashedFirstName', 'hashedLastName', 'hashedPhoneNumber'
    ]].to_dict(orient='records')
    
    return {
        'rawData': {
            'contact_info_list': contact_info_list
        }
    }
    
