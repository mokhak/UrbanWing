import streamlit as st
import requests
from datetime import datetime
from PIL import Image
import io
from pymongo import MongoClient
import random


AUTH_SERVICE_URL = "http://localhost:5005/authenticate"

st.set_page_config(
    page_title="Login",
    page_icon="logo.png",
    layout="centered",    
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None
    

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
                # st.success("Login Successful!")
                st.switch_page('home.py')
            else:
                st.error("Invalid credentials!")
        except Exception as e:
            st.error(f"str(e)")
    else:
        st.warning("Please enter both username and password!")