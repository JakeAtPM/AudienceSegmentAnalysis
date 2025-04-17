import openai
import os
from dotenv import load_dotenv
import streamlit as st

#api key
# load_dotenv('.env')
# openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = st.secrets['OPENAI_API_KEY']


#My idea is that this will run last before the final JSON is sent through Jinja2, to the html output
# All of the other fields are filled out and when they select "finished" (or something similar) it is ran through this json summary function, the ai summary is sent to the final json file, which is then sent to jinja and the report in populated and output 

def generate_summary(initial_json_output):
    prompt = f"""
Looking only at the 'title' part of the JSON given, analyze and give a short (approx. 100 word) summary about the audience segment described in the data. Don't introduce the segment. The summary should be professional, concise, and suitable for a marketing report.

json file: {initial_json_output}
"""
    response = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role':'user','content':prompt}],
        temperature = 0.7,
        max_tokens = 300
        )
    
    summary_text = response.choices[0].message.content.strip()


    return summary_text