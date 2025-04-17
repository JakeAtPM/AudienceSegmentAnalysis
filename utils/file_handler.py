import os
import pandas as pd
from pathlib import Path
import re
import base64
import mimetypes


# Define upload directories
UPLOAD_DIR = Path('data/uploads')
IMAGE_DIR = Path("static/images/uploads")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_filename(filename):
    # Replace unsafe characters with _
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def save_and_load_upload(uploaded_file):
    """
    Save uploaded CSV/XLSX and return as a DataFrame.
    """
    filename = sanitize_filename(uploaded_file.name)
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if filename.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")
    
    return df

def save_uploaded_image(image_file):
    """
    Save an uploaded image and return the path.
    """
    filename = sanitize_filename(image_file.name)
    image_path = IMAGE_DIR / filename

    with open(image_path, "wb") as f:
        f.write(image_file.read())

    return str(image_path)

def get_path(file_name, folder="data/uploads"):
    """
    Return the full path to a file in a given folder.
    """
    return str(Path(folder) / sanitize_filename(file_name))


def encode_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
        mime_type, _ = mimetypes.guess_type(image_path)
        return f"data:{mime_type};base64,{encoded}"