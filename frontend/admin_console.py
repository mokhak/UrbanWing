import streamlit as st
from pymongo import MongoClient
import requests
from endpoint_url import AUTH_SERVICE_URL, CAMERA_SERVICE_URL
from PIL import Image
from io import BytesIO

st.title("🦉 Hello Admin!")

st.divider()

st.subheader("📸 Run Camera Service")

# Fetch emails on button click
headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
if st.button("Get All User Data"):
    response = requests.get(
        AUTH_SERVICE_URL + "/getallusers",
        headers=headers,
        json={"role": st.session_state.current_user_data["role"]}
    )

    if response.status_code == 200:
        data = response.json()
        st.session_state["emails"] = [item["email"] for item in data]  # Store emails in session state
        st.success("User data fetched successfully!")
    else:
        error = response.json()["msg"]
        st.error(f"Failed to fetch user data. {error}!")

# Display selectbox only if emails are available
if st.session_state["emails"]:
    user_selection = st.selectbox(
        "Select User",
        st.session_state["emails"],
        index=st.session_state["emails"].index(st.session_state["user_selection"])
        if st.session_state["user_selection"] in st.session_state["emails"]
        else 0
    )

    # Store the selected user in session state
    st.session_state["user_selection"] = user_selection
    if st.button("Post Image"):
        response = requests.post(
            CAMERA_SERVICE_URL + "/upload-image",
            headers=headers,
            json={"role": st.session_state.current_user_data["role"],
                  "useremail": st.session_state["user_selection"]}
        )
        if response.status_code == 200:
            st.success("Posted Image on User Account!")
        else:
            st.error(f"Unable to post image. Status code: {response}")

else:
    st.warning("No user data available. Click the button above to fetch user data.")
    
st.divider()

st.subheader("API Endpoint Statistics")
    
