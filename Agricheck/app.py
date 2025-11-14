import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Configure the page first
st.set_page_config(
    page_title="Agricheck - Plant Disease Detector",
    page_icon="🌿",
    layout="centered"
)

# App title
st.title("🌿 Agricheck")
st.subheader("AI-Powered Plant Disease Detection for Kenyan Farmers")

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error(" Gemini API key not found. Please check your .env file")
    st.stop()

try:
    genai.configure(api_key=api_key)
    # Use the correct model from your available list
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    st.success(" Using model: Gemini 2.0 Flash - Perfect for image analysis!")
except Exception as e:
    st.error(f" Failed to configure Gemini: {str(e)}")
    st.stop()

# Our MAGIC PROMPT - Enhanced for better results
PLANT_EXPERT_PROMPT = """
You are AgriBot, an expert agronomist specializing in organic farming in Kenya. 

Analyze the provided image of a plant leaf and provide a comprehensive diagnosis:

**DISEASE IDENTIFICATION**: 
- Name the most likely plant disease
- Identify the plant species if possible

**SYMPTOM ANALYSIS**: 
- Describe the visible symptoms (spots, discoloration, patterns)
- Note the location and pattern of damage

**ORGANIC TREATMENT PLAN**:
- Provide 2-3 simple, organic treatment steps
- Use remedies available in Kenya (neem oil, baking soda, ash, etc.)
- Include preparation and application instructions

**PREVENTION TIPS**:
- 2-3 cultural practices to prevent recurrence
- Advice on spacing, watering, and soil health

If the image is unclear or not a plant leaf, politely ask for a better image.

Keep responses practical, actionable, and focused on small-scale Kenyan farmers.
"""

def analyze_plant_disease(image):
    """Analyze the plant image using Gemini AI"""
    try:
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        st.info("🔄 Sending to Gemini AI for analysis...")
        
        # Generate content
        response = model.generate_content([
            PLANT_EXPERT_PROMPT,
            {"mime_type": "image/jpeg", "data": img_byte_arr}
        ])
        
        return response.text
        
    except Exception as e:
        return f" Error analyzing image: {str(e)}"

# Test connection
def test_gemini_connection():
    try:
        test_response = model.generate_content("Say 'Habari from Agricheck!' and nothing else.")
        return f" API Working: {test_response.text}"
    except Exception as e:
        return f" API Failed: {str(e)}"

# Sidebar with info
with st.sidebar:
    st.header("🌱 About Agricheck")
    st.write("""
    **How to use:**
    1.  Take clear photo of diseased leaf
    2.  Upload image
    3.  Click 'Analyze Disease'
    4.  Get organic treatment advice!
    
    """)
    
    st.divider()
    
    if st.button("Test Connection"):
        result = test_gemini_connection()
        st.write(result)

# Main app interface
st.write("Upload a clear photo of a plant leaf to identify diseases and get organic treatment advice.")

uploaded_file = st.file_uploader(
    "Choose an image file", 
    type=['jpg', 'jpeg', 'png'],
    help="Take a clear photo of the diseased plant leaf"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Plant Leaf", use_column_width=True)
    st.success(" Image uploaded successfully!")
    
    if st.button(" Analyze Disease", type="primary"):
        with st.spinner(" AI is analyzing the plant health... This may take 10-20 seconds."):
            result = analyze_plant_disease(image)
        
        st.header(" Analysis Results")
        
        # Display results in a nice box
        st.success("Analysis Complete!")
        st.write(result)
        
        st.info(" **Remember**: This is AI-assisted advice. For serious crop issues, consult local agricultural experts.")
else:
    st.info(" Please upload an image of a plant leaf to get started")