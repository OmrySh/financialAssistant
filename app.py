import streamlit as st
from PIL import Image

import financial_assistasnt_page
import signup_page
import welcome_page
import login_page
from utils import local_css



app_symbol = Image.open("images/app_symbol.jpg")
st.set_page_config(page_title="EconoMe", layout="wide", page_icon=app_symbol)
local_css("style/style.css")
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/\nst.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")
# Initialize session state for current page if not already set
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'welcome'
if 'logged_username' not in st.session_state:
    st.session_state['logged_username'] = 'None'
if 'logged_username_info' not in st.session_state:
    st.session_state['logged_username_info'] = 'None'
if 'feedback_received' not in st.session_state:
    st.session_state['feedback_received'] = False



# ---- LOAD ASSETS ----

img_contact_form = Image.open("images/yt_contact_form.png")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")


# Main app logic to show different pages based on the current state
if st.session_state['current_page'] == 'welcome':
    welcome_page.show()
elif st.session_state['current_page'] == 'login':
    login_page.show()
elif st.session_state['current_page'] == 'signup':
    signup_page.show()
elif st.session_state['current_page'] == 'assistant':
    financial_assistasnt_page.show()
