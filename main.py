import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "signup_display" not in st.session_state:
    st.session_state.signup_display = False
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "current_user_data" not in st.session_state:
    st.session_state.current_user_data = None
if "welcome_message" not in st.session_state:
    st.session_state.welcome_message = None
    
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.signup_display = False
    st.session_state.current_user_data = None
    st.rerun()
        
logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
    
entry_page = st.Page("frontend/entry.py", title="Log in")
home_page = st.Page("frontend/home.py", title="Home", icon=":material/dashboard:")
admin_page = st.Page("frontend/admin_console.py", title="Admin Console")

if st.session_state.logged_in:
    if st.session_state.current_user_data["role"] == "sysadmin":
        pg = st.navigation(
        {
            "Navigation": [admin_page],
            "Account": [logout_page], 
        }
    )
    elif st.session_state.current_user_data["role"] == "Regular":
        pg = st.navigation(
            {
                "Navigation": [home_page],
                "Account": [logout_page],
            }
        )
else:
    pg = st.navigation([entry_page])

pg.run()