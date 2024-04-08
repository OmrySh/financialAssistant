import streamlit as st
import json
from utils import navigate_to


def check_credentials(username, password):
    """Check if the credentials match any existing ones in the credentials JSON file."""
    credentials_file_path = "credentials.json"
    try:
        with open(credentials_file_path, "r") as file:
            users = json.load(file)
            # Check if the username exists and the password matches
            user = users.get(username)
            if user and user.get("password") == password:
                st.session_state['logged_username_info'] = user
                return True
        return False
    except FileNotFoundError:
        return False


def show():

    st.subheader("Login")
    col1, _ = st.columns([1, 1])
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

    st.markdown("""
                   <style>
                   button {
                       width: 80px !important;
                       margin: 10px 0px !important;
                       padding: 0px !important; /* Minimize padding to help control height */
                       line-height: 20px !important; /* Adjust line height to vertically center text */
                   }
                   </style>
                   """, unsafe_allow_html=True)

    button1, button2, _ = st.columns((1, 1, 3))
    with button1:
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state['logged_username'] = username
                navigate_to("assistant")
            else:
                st.error("Invalid username or password")
    with button2:
        if st.button("Back"):
            navigate_to('welcome')