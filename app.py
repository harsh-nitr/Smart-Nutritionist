import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Calories Advisor APP")

st.header("Calories Advisor APP")

uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert nutritionist. Analyze the food items in the image and estimate 
the total calorie count. Also, provide details of each food item with its calorie intake 
in the following format:

1. Item 1 - no. of calories
2. Item 2 - no. of calories
----
----
Finally, mention whether the food is healthy or not and also provide 
the percentage split of carbohydrates, fats, fibers, sugar, and other 
necessary dietary components.
"""

if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("The response is:")
        st.write(response)
    else:
        st.error("Please upload an image before submitting.")
