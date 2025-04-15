import streamlit as st
import openai
import json
import io
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# --- Streamlit App Title ---
st.set_page_config(page_title="Audience Segment Summary Generator", layout="centered")
st.title("📊 Audience Segment Summary Generator")

# --- Text Input ---
input_blurb = st.text_area("Enter a short audience blurb", height=150, placeholder="e.g., Young professionals in tech who value sustainability and shop online for luxury basics.")

# --- Generate Button ---
if st.button("Generate Summary"):
    if not input_blurb.strip():
        st.warning("⚠️ Please enter an audience blurb before proceeding.")
    else:
        with st.spinner("Generating summary with ChatGPT..."):
            try:
                # --- Build Prompt ---
                prompt = f"""
Please generate a professional audience segment summary based on the following blurb. 
The summary should be formal, concise, and suitable for a marketing report. 
Highlight demographic, behavioral, and psychographic traits where relevant.

Input blurb: "{input_blurb}"
"""

                # --- Call OpenAI ChatGPT ---
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )

                summary_text = response.choices[0].message["content"].strip()

                # --- Display the Result ---
                st.success("✅ Generated Summary:")
                st.write(summary_text)

                # --- Prepare JSON Output ---
                summary_json = {
                    "input_blurb": input_blurb,
                    "generated_summary": summary_text,
                    "timestamp": datetime.now().isoformat()
                }

                # --- Filename & Download Button ---
                filename = f"audience_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                json_str = json.dumps(summary_json, indent=2)
                json_bytes = io.BytesIO(json_str.encode('utf-8'))

                st.download_button(
                    label="📥 Download Summary as JSON",
                    data=json_bytes,
                    file_name=filename,
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"❌ Error generating summary: {e}")
