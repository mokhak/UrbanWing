import streamlit as st
import random
from PIL import Image

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

