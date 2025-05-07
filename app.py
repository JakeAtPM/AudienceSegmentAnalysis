import os
import streamlit as st
import json
from jinja2 import Environment, FileSystemLoader
import io
from datetime import datetime
import base64
import zipfile

from utils import ai_summarize, gcs_api_client, L2_api_client, file_handler

# Initialize session state
if "html_bytes" not in st.session_state:
    st.session_state["html_bytes"] = ''
    st.session_state["html_filename"] = ''

if "json_bytes" not in st.session_state:
    st.session_state["json_bytes"] = ''
    st.session_state["json_filename"] = ''

st.set_page_config(page_title="Audience Segment Report", layout="wide")
st.title("📊 Audience Segment Report Builder")

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Report Builder",
    "⚙️ Advanced Inputs",
    "🌐 API Tools",
    "🧠 Generate Report"
])

# ---------------- Tab 1: Report Basics ----------------
with tab1:
    st.subheader('📝 Report Basics')
    
    audience_title = st.text_input("📝 Audience Title", help="This will appear as the report title")

    # Primary News Outlets Input
    st.subheader("📰 Primary News Outlets")
    news_outlets = st.text_area("Enter each news outlet on a new line").splitlines()

    # High-Affinity Keywords Input
    st.subheader("🔑 High-Affinity Keywords")
    keywords = st.text_area("Enter each keyword on a new line")

    # Recommended Media Targets Input
    st.subheader("🎯 Media Targets")
    media_targets = []
    num_targets = st.number_input("How many media targets?", min_value=1, max_value=10, step=1)
    for i in range(num_targets):
        with st.expander(f"Media Target #{i+1}"):
            org = st.text_input(f"Target #{i+1} - Organization Name", key=f"media_org_{i}")
            desc = st.text_area(f"Target #{i+1} - Description", key=f"media_desc_{i}")
            media_targets.append({"organization": org, "description": desc})

    # Places of Interest Input
    st.subheader("📍 Places of Interest")
    places = st.text_area("Enter each place of interest on a new line").splitlines()


    # Media Categories Input
    st.subheader("📂 Media Categories Visited")
    categories = st.text_area("Enter each category on a new line").splitlines()


    # Target Audience Demographics Input
    st.subheader("PLACEHOLDER IMAGE TEST")
    image_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])

    if image_file:
        saved_path = file_handler.save_uploaded_image(image_file)
        image_base64 = file_handler.encode_image_base64(saved_path)
        st.image(saved_path, caption="Uploaded demographic image", use_container_width=True)
    else:
        saved_path = None
        image_base64 = None


# ---------------- Tab 4: Generate Report ----------------
with tab4:
    st.subheader("🧠 Generate Audience Report")

    # Logo hard-encoded into html
    logo_base64 = file_handler.encode_image_base64('static/images/publicmedia-logo.png')
    
    with st.expander("📁 Load Existing JSON (if you have it)"):
        uploaded_json = st.file_uploader("Upload a previously generated JSON file", type="json")
        if uploaded_json is not None:
            report_data = json.load(uploaded_json)

            # Render HTML with Jinja2
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template("report_template_v3.html")
            html_output = template.render(report=report_data)

            # Save to temporary HTML file
            html_file_name = f"{report_data['title'].replace(' ', '_')}_report_from_json.html"
            with open(html_file_name, "w") as f:
                f.write(html_output)

            # Show preview & download
            st.success("Report generated from uploaded JSON!")
            st.download_button(
                label="📥 Download HTML Report",
                data=open(html_file_name, "rb"),
                file_name=html_file_name,
                mime="text/html"
            )
            
    if st.button("✅ Generate Report"):
        # Clean and prepare user input
        cleaned_keywords = [k.strip() for k in keywords.splitlines() if k.strip()]

        report_data = {
            "title": audience_title,
            "news_outlets": news_outlets,
            "keywords": cleaned_keywords,
            "media_targets": media_targets,
            "places_of_interest": places,
            "media_categories": categories,
        }

        with st.spinner("Generating summary with AI..."):
            summary_text = ai_summarize.generate_summary(report_data)
            report_data["summary"] = summary_text

        # Render HTML with Jinja2
        report_data['logo_base64'] = logo_base64
        report_data['demographic_image'] = image_base64

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template("report_template_v3.html")
        html_output = template.render(report=report_data)

        # Ensure output directory exists
        output_dir = "output/reports"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{audience_title.replace(' ', '_')}_report.html")

        with open(output_path, "w") as f:
            f.write(html_output)

        # Read HTML content into session state
        with open(output_path, "rb") as f:
            st.session_state["html_bytes"] = f.read()
            st.session_state["html_filename"] = os.path.basename(output_path)

        # Save JSON file and read into session state
        json_output_dir = "json/generated_json"
        os.makedirs(json_output_dir, exist_ok=True)
        json_output_path = os.path.join(json_output_dir, f"{audience_title.replace(' ', '_')}.json")

        with open(json_output_path, "w") as f:
            json.dump(report_data, f, indent=2)

        with open(json_output_path, "rb") as jf:
            st.session_state["json_bytes"] = jf.read()
            st.session_state["json_filename"] = os.path.basename(json_output_path)

        st.success("✅ Report generated!")
        st.json(report_data, expanded=False)
        st.info('Download the report below!') 
        
        # Formatting Gap
        st.write("")

        # Only create the zip if both HTML and JSON exist
        if st.session_state["html_bytes"] and st.session_state["json_bytes"]:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(st.session_state["html_filename"], st.session_state["html_bytes"])
                zip_file.writestr(st.session_state["json_filename"], st.session_state["json_bytes"])

            zip_buffer.seek(0)
            
            safe_title = audience_title.strip().replace(' ', '_').replace('/','_') if audience_title else "AudienceSegmentReport"
            zip_filename = f'{safe_title}_Report.zip'
            
            st.download_button(
                label="📦 Download Report Bundle (HTML + JSON)",
                data=zip_buffer,
                file_name=zip_filename,
                mime="application/zip"
            )