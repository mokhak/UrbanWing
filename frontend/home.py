import streamlit as st
import random
from PIL import Image
import requests
from endpoint_url import CAMERA_SERVICE_URL
from io import BytesIO
import time

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

welcome_message = random.choice(WELCOME_MESSAGES).format(username=st.session_state.current_user_data["firstname"])
st.markdown(
    f"""
    <h2 style='text-align: center;'>{welcome_message}</h2>
    </p>
    """,
    unsafe_allow_html=True
)



st.divider()

headers = {"Authorization": f"Bearer {st.session_state.access_token}"}

response = requests.get(
    CAMERA_SERVICE_URL + "/get-latest-visitor",
    headers=headers,
    json={"email": st.session_state.current_user_data["email"]}
)
if response.status_code == 200:
    image_url = response.json()["imageurl"]
    classification_status = response.json()["classification_status"]
    classification = response.json()["classification"]
    
    image_req = requests.get(image_url)
    if image_req.status_code == 200:
        image = Image.open(BytesIO(image_req.content))
    
    st.subheader("🐦 While you were away, a curious little visitor dropped by! See who fluttered in! 🌿✨")
    st.write(f"Species Identification: {classification}")
    resized_image = image.resize((400,400))
    st.image(resized_image, use_container_width=True)
    
else:
    st.error(response.json["error"])