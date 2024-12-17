import streamlit as st
from streamlit_lottie import st_lottie
import bcrypt
import requests
from endpoint_url import AUTH_SERVICE_URL
import time

st.markdown("""
            <h1 style='text-align: center; color: #2E8B57; font-size:50px;'>🕊️ Welcome to UrbanWing! 🕊️\
                <h4 style='text-align: center; color: gray;'>Bringing Nature Closer, One Feathered Friend at a Time.</h3>\
                    </h1>
            </p>
            """,
            unsafe_allow_html=True
)
st.divider()

def login_elements():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    sign_in = st.button("🐣 Chirp In")
    st.write("")
    st.write("")        
    st.write("New to the flock? Click the button below to join and start your birding adventure!")
    if st.button("🪺 Join the Nest"):
        st.session_state.signup_display = True
        st.rerun()
        
    if sign_in:
        if username and password:
            if login_user(username, password):
                st.success("Login Successful!")
                st_lottie("https://lottie.host/071500ca-4d90-467d-95cd-025b6974c4c2/0KgqWnQaN5.json", loop=False)
                time.sleep(1)
                st.rerun()

            else:
                st.error(f"Invalid credentials! Are you a new user? \
                    Create an account by clicking the button below.")

        else:
            st.warning("Please enter both username and password!")

def signup_elements():
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    sign_up = st.button("🪺 Join the Nest")
    st.write("")
    st.write("")
    st.write("Already part of the flock? Click the button below to hop into your nest!")
    if st.button("🐣 Chirp In"):
        st.session_state.signup_display = False
        st.rerun()
        
    if sign_up:
        if first_name and last_name and email and username and password and confirm_password:
            if password == confirm_password:
                encrypt_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                response = requests.post(
                    AUTH_SERVICE_URL + "/createuser", json = {
                        "firstname": first_name,
                        "lastname": last_name,
                        "email": email,
                        "username": username,
                        "password": encrypt_pass
                    }
                )
                if response.status_code == 401:
                    st.error("Your Email is already registered! Please try to Login.")
                elif response.status_code == 402:
                    st.error("This username is already in use! Please try a different username.")
                elif response.status_code == 200:
                    st.success("You are registered!")
                    login_user(username, password)
                    st_lottie("https://lottie.host/071500ca-4d90-467d-95cd-025b6974c4c2/0KgqWnQaN5.json", loop=False)
                    time.sleep(1)
                    st.rerun()
                    
            else:
                st.error("Please make sure both passwords match!")
        else:
            st.error("Please fill out all the fields!")
            
            
def login_user(username, password):
    response = requests.get(
        AUTH_SERVICE_URL + "/authenticate", json={"username": username, "password": password}
    )
    if response.status_code == 200:
        st.session_state.logged_in = True
        st.session_state.access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.get(
            AUTH_SERVICE_URL + "/getuserinfo", headers=headers
        )
        st.session_state.current_user_data = response.json()
        
        return True
    else:
        st.write(response.status_code)
        return False
    
        
if st.session_state.signup_display == False:
    login_elements()
else:
    signup_elements()

    