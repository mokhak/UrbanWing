import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "signup_display" not in st.session_state:
    st.session_state.signup_display = False
    
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.signup_display = False
    st.rerun()
        
logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
    
entry_page = st.Page("frontend/entry.py", title="Log in")
home_page = st.Page("frontend/home.py", title="Home", icon=":material/dashboard:", default=True)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "": [logout_page],
            "Home": [home_page],
        }
    )
else:
    pg = st.navigation([entry_page])

pg.run()