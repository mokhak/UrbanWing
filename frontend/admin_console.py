import streamlit as st
from pymongo import MongoClient
import requests
from endpoint_url import AUTH_SERVICE_URL

st.title("🦉 Hello Admin!")

st.divider()

st.subheader("📸 Run Camera Service")

headers = {"Authorization": f"Bearer {st.session_state.access_token}",
           "firstname": st.session_state.current_user_data["firstname"]}
response = requests.get(
    AUTH_SERVICE_URL + "/getallusers", headers=headers
)
st.write(headers)
st.write(response)