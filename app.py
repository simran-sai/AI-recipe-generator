import streamlit as st
import google.generativeai as ga
import pathlib as Path
from api_key import api_key
import os
import tempfile
import PIL.Image

# Configure genai with api keys
ga.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Set up safety settings
safety_settings=[
    {
        "category":"HARM_CATEGORY_HARASSMENT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_HATE_SPEECH",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"

    },

]

# Model configuration
model = ga.GenerativeModel('gemini-1.5-pro', generation_config=generation_config, safety_settings=safety_settings)
st.set_page_config(page_title="AI Recipe Generator", page_icon="🍽", layout="wide")
st.title("AI Recipe Generator")

st.image("logo.png", width=150)
st.subheader("Upload an image to generate a recipe")

uploaded_file = st.file_uploader("Upload a dish image to generate a recipe!", type=["png", "jpg", "jpeg"])
submit=st.button("Analyze Image")

if submit:
        img = uploaded_file.getvalue()
        newimage = PIL.Image.open(uploaded_file)
        prompt = "Tell me the recipe of this dish in detail"
        response = model.generate_content([prompt, newimage], stream=True)
        response.resolve()
        st.write(response.text)