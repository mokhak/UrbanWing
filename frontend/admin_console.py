import streamlit as st
from pymongo import MongoClient
import requests
from endpoint_url import AUTH_SERVICE_URL, CAMERA_SERVICE_URL
from PIL import Image
from io import BytesIO
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
# MongoDB Connection
mongo_uri = os.getenv("MONGO_URI")
DATABASE_NAME = "auth_database"
COLLECTION_NAME = "endpoint_stats"

st.title("🦉 Hello Admin!")

st.divider()

st.header("📸 Run Camera Service")

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

# Function to fetch usage statistics
def fetch_usage_statistics():
    client = MongoClient(mongo_uri)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    stats = list(collection.find())
    client.close()
    return stats

# Process data
def process_data(stats, selected_service=None):
    df = pd.DataFrame(stats)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if "_id" in df.columns:
        df = df.drop(columns=["_id"])
    if selected_service:
        df = df[df["service"] == selected_service]
    return df

# Streamlit Dashboard
st.header("📊 API Usage and Performance Statistics")

# Fetch usage statistics
stats = fetch_usage_statistics()

if stats:
    # Process data
    df = process_data(stats)

    # Service Selection
    services = list(df["service"].unique())
    selected_service = st.selectbox("Select Service", ["All"] + services)

    # Filter data by service
    filtered_df = df if selected_service == "All" else df[df["service"] == selected_service]

    # Display Summary Statistics
    st.header("Summary Statistics")
    st.write(f"**Total Requests:** {len(filtered_df)}")
    st.write(f"**Unique Endpoints:** {filtered_df['endpoint'].nunique()}")

    # Average Execution Time by Endpoint
    st.subheader("Average Execution Time by Endpoint")
    avg_time = filtered_df.groupby("endpoint")["execution_time"].mean().sort_values()
    st.bar_chart(avg_time)

    # Slowest Endpoints
    st.subheader("Top 5 Slowest Endpoints")
    slowest_endpoints = avg_time.sort_values(ascending=False).head(5)
    st.table(slowest_endpoints.reset_index().rename(columns={"execution_time": "Average Time (s)"}))

    # Requests Over Time
    st.subheader("Requests Over Time")
    requests_over_time = filtered_df.resample("1Min", on="timestamp").size()
    st.line_chart(requests_over_time)

    # Raw Data
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df)

else:
    st.warning("No data available. Make sure the services are running and logging stats.")
    
