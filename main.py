import streamlit as st

pages = {
    "": [
        st.Page('frontend/home.py', title='Home', icon=':material/home:'),
    ],
}
pg = st.navigation(pages)
pg.run()