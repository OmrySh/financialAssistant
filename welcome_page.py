import streamlit as st
from streamlit_lottie import st_lottie
from utils import navigate_to, load_lottieurl

lottie_coding = load_lottieurl("https://lottie.host/fe99b3f0-ef70-457b-ac24-9520f5ecc05e/yihgioLLyl.json")

def show():
    import os

    # Print the current working directory
    st.write("Current working directory:", os.getcwd())

    # List files in the expected directory
    expenses_dir = 'expenses_data'
    if os.path.isdir(expenses_dir):
        st.write("Files in expenses_data:", os.listdir(expenses_dir))
    else:
        st.write(f"Directory {expenses_dir} not found")

    # ---- HEADER SECTION ----
    with st.container():
        st.subheader("Welcome to EconoMe - Your Financial Assistant :wave:")
        st.title("The Place Where You Can Learn About Your Money, Savings, and Investments")
        st.write(
            "Using Your Financial Data, the Financial Assistant Will Help Learn New Financial Topics "
            "That Will Help You Make Decisions and Plan for the Future."
        )

    # ---- WHAT I DO ----
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("How Does it Work?")
            st.write("##")
            st.write(
                """
                - EconoMe uses your financial data to provide you with personalized videos questions, news and simulator.\n
                - EconoMe also helps you understand the basics of personal finance and investing using videos and games.\n
                - EconoMe is designed to be easy to use and accessible to everyone."""
            )
        with right_column:
            st_lottie(lottie_coding, height=300, key="coding")

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

    login_butt, sign_butt, _ = st.columns((1,1,3))
    with login_butt:
        if st.button("Login"):
            navigate_to('login')

    with sign_butt:
        if st.button("Sign Up"):
            navigate_to('signup')