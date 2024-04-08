import streamlit as st
from streamlit_lottie import st_lottie
import expenses_anlysis_page
import games_page
import news_page
import simulator_page
import videos_page
import recommender
from utils import update_fields_in_user_info, load_user_info, load_lottieurl
import model
import json
import os
from model import Model


def save_uploaded_file(uploaded_file, username):
    # Define the directory path where files will be stored
    directory_path = 'expenses_data'

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Define the full path for the new file
    file_path = os.path.join(directory_path, f'{username}_expenses.csv')

    # Write the uploaded file to the new file path
    with open(file_path, "wb") as f:
        # Streamlit uploaded files are binary, use .getbuffer() for BytesIO
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved to {file_path}.")
    return file_path


def show():
    # ---- UPLOAD YOUR EXPENSE DATA ----
    username = st.session_state['logged_username']
    lottie_coding = load_lottieurl("https://lottie.host/fe99b3f0-ef70-457b-ac24-9520f5ecc05e/yihgioLLyl.json")

    header_col, lottie_col, _ = st.columns((2, 1, 5))
    with header_col:
        st.header(f"Hi There {username}!")
    with lottie_col:
        st_lottie(lottie_coding, key="hi_there", height=100)

    user_info = load_user_info(username)
    if 'expenses_path' not in user_info:
        st.header("Upload Your Expenses")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file, username)
            model_prediction = model.run_model(username)
            update_fields_in_user_info(username, {'expenses_path': file_path,
                                                  'present_videos': [],
                                                  'liked_video': [],
                                                  'unliked_video': [],
                                                  'present_questions': [],
                                                  'right_questions': [],
                                                  'wrong_questions': []
                                                  }
                                       )
            update_fields_in_user_info(username, model_prediction)
            st.rerun()

    # if uploaded_file is not None:
    else:
        if 'show_content' not in st.session_state:
            st.session_state['show_content'] = None

        st.markdown("""
        <style>
        button {
            width: 100% !important;
            height: 60px !important; /* Attempt to set a fixed height */
            margin: 10px 0px !important;
            padding: 0px !important; /* Minimize padding to help control height */
            line-height: 20px !important; /* Adjust line height to vertically center text */
        }
        </style>
        """, unsafe_allow_html=True)

        buttons_col, content_col = st.columns((1, 10))
        if st.sidebar.button("Recommended Videos"):
            st.session_state['show_content'] = 'videos'

        if st.sidebar.button("Quiz"):
            st.session_state['show_content'] = 'games'

        if st.sidebar.button("Simulator"):
            st.session_state['show_content'] = 'Simulator'

        if st.sidebar.button("News"):
            st.session_state['show_content'] = 'News'

        uploaded_file = st.sidebar.file_uploader("Upload Your Updated Expenses", type="csv")
        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file, username)
            update_fields_in_user_info(username, {'expenses_path': file_path})
            model_prediction = model.run_model(username)
            update_fields_in_user_info(username, model_prediction)

        if st.session_state['show_content'] == 'videos' or st.session_state['feedback_received']:
            st.session_state['feedback_received'] = False
            videos_page.show_recommended_videos()

        elif st.session_state['show_content'] == 'games':
            games_page.show_financial_quiz()

        elif st.session_state['show_content'] == 'Analysis':
            expenses_anlysis_page.show()

        elif st.session_state['show_content'] == 'News':
            news_page.show()

        elif st.session_state['show_content'] == 'Simulator':
            simulator_page.show()

    # ---- CONTACT ----
    with st.container():
        st.write("---")
        st.header("Get In Touch With Us!")
        st.write("##")

        # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
        contact_form = """
        <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st.empty()
