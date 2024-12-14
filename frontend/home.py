import streamlit as st
import requests
from datetime import datetime
from PIL import Image
import io
from pymongo import MongoClient
import random

import time

# API Endpoints
CAMERA_SERVICE_URL = "http://localhost:5004/upload-image"
CLASSIFICATION_SERVICE_URL = "http://localhost:5003/classify-image"
MONGODB_URL = "mongodb://localhost:27017"
AUTH_SERVICE_URL = "http://localhost:5005/authenticate"

st.set_page_config(
    page_title="UrbanWing",
    page_icon="logo.png",
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None
    
def login_page():
    st.markdown("""
                <h1 style='text-align: center; color: #2E8B57; font-size:50px;'>🕊️ Welcome to UrbanWing! 🕊️\
                    <h4 style='text-align: center; color: gray;'>Bringing Nature Closer, One Feathered Friend at a Time.</h3>\
                        </h1>
                </p>
                """,
                unsafe_allow_html=True
    )
    
    # st.subheader('🐣 Chirp In')
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("🐣 Chirp In"):
        if username and password:
            try:
                response = requests.post(
                    AUTH_SERVICE_URL, json={"username": username, "password": password}
                )
                if response.status_code == 200 and response.json()["success"]:
                    st.session_state.logged_in = True
                    st.session_state.username = "Kirat"
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
            except Exception as e:
                st.error(f"str(e)")
        else:
            st.warning("Please enter both username and password!")

client = MongoClient(MONGODB_URL)
db = client["image_database"]
# Streamlit UI
def main_app(username):
    WELCOME_MESSAGES = [
    "🦜🌟 Welcome back, {username}! Ready to spread your wings today? 🐾✨",
    "🐦💬 Chirp, chirp! Great to see you, {username}! The birds are waiting for you. 🌿🌈",
    "🪶☁️ Hi, {username}! The skies are calling. Let's spot some feathered friends! 🕊️🎉",
    "🦉🍃 Hello, {username}! Perch yourself comfortably and enjoy bird-watching. 🌸🔭",
    "🐤🍂 Welcome, {username}! Let's flock together and explore the beauty of nature. 🌼🦚",
    "🕊️🌞 Hi, {username}! A new day, a new flock. Let's take flight into birdwatching! 🌺🐧",
    "🐔🍁 Good to see you, {username}! The UrbanWing awaits your watchful eye. 🌟🦅",
    "🪺🌿 Nestled in nicely, {username}? Time to catch the chirping beauties! 🌷🐥",
    "🌈✨ Hello, {username}! The garden's alive with feathers and songs. 🌳🦜",
    "🌟🪹 Greetings, {username}! Every wingbeat tells a story—let's discover them together. 🐦🍀"
    ]
    
    welcome_message = random.choice(WELCOME_MESSAGES).format(username=username)
    st.markdown(
        f"""
        <h2 style='text-align: center;'>{welcome_message}</h2>
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.write(
        "Home",
        ["home"]
        )

    # Image Upload
    st.subheader("Upload an Image to Simulate the Camera")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    # State Management
    if "last_uploaded_filename" not in st.session_state:
        st.session_state.last_uploaded_filename = None

    if uploaded_file:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        with open("temp_uploaded_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Upload to Camera Service
        if st.button("Upload to Camera Service"):
            try:
                # Upload the image to the camera service
                with open("temp_uploaded_image.jpg", "rb") as img:
                    response = requests.post(
                        CAMERA_SERVICE_URL,
                        files={"image": img}
                    )
                if response.status_code == 201:
                    result = response.json()
                    st.success("Image successfully uploaded to the camera service!")
                    st.session_state.last_uploaded_filename = result["filename"]
                    st.write(f"Image Name: {result['filename']}")
                    st.write(f"Timestamp: {result['timestamp']}")
                else:
                    st.error(f"Failed to upload image. Error: {response.text}")
            except Exception as e:
                st.error(f"Error while uploading image: {str(e)}")

    # Analyze Image
    if st.session_state.last_uploaded_filename:
        st.subheader("Analyze the Last Uploaded Image")
        if st.button("Analyze Image"):
            try:
                # Call the classification service
                response = requests.post(
                    CLASSIFICATION_SERVICE_URL,
                    json={"image_name": st.session_state.last_uploaded_filename}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Image successfully analyzed!")
                    st.write(f"Bird Detected: {result['bird_detected']}")
                    st.write(f"Bird Type: {result['bird_type']}")
                    st.write(f"Confidence: {result['confidence']}")
                else:
                    st.error(f"Failed to analyze image. Error: {response.text}")
            except Exception as e:
                st.error(f"Error while analyzing image: {str(e)}")
                
    st.subheader("Database Entries")
    if st.button("Show All Entries"):
        try:
            entries = db.fs.files.find()
            for entry in entries:
                st.write({
                    "filename": entry["filename"],
                    "timestamp": entry.get("timestamp"),
                    "bird_detected": entry.get("bird_detected"),
                    "bird_type": entry.get("bird_type"),
                    "confidence": entry.get("confidence")
                })
        except Exception as e:
            st.error(f"Error while fetching database entries: {str(e)}")
    if st.button("logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    # Show a temporary notification
    if st.button("Show Temporary Notification"):
        st.toast("hello!")

if not st.session_state.logged_in:
    login_page()
else:
    main_app("Kirat")
    