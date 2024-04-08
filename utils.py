import requests
import streamlit as st
import json
from youtubesearchpython import VideosSearch


# Helper function to navigate
def navigate_to(page_name):
    st.session_state['current_page'] = page_name
    st.rerun()


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def search_youtube(topic):
    videos_search = VideosSearch(topic, limit = 1)
    results = videos_search.result()

    if results['result']:
        first_video = results['result'][0]
        print(first_video)
        video_link = first_video['link']
        image_link = first_video['thumbnails'][0]['url']
        title = first_video['title']
        return video_link, image_link, title
    else:
        return "No videos found."



def load_user_info(username):
    """Load user's info dictionary by username"""
    credentials_file_path = "credentials.json"

    try:
        # Load the existing users data
        with open(credentials_file_path, "r") as file:
            users = json.load(file)

        if username in users:
            return users[username]
        else:
            print(f"User '{username}' not found.")
    except FileNotFoundError:
        print(f"File '{credentials_file_path}' not found.")


def update_fields_in_user_info(username, field_dictionary):
    """Add a new field to an existing user's information in the JSON credentials file."""
    credentials_file_path = "credentials.json"

    try:
        # Load the existing users data
        with open(credentials_file_path, "r") as file:
            users = json.load(file)

        # Check if the user exists
        if username in users:
            # Update the user's info with the new field
            user_info = users[username]
            for field in field_dictionary:

                # in case the field doesn't exist or not a list
                if field not in user_info or not isinstance(user_info[field], list):
                    user_info[field] = field_dictionary[field]

                # in case the field exist and is list
                else:
                    if isinstance(field_dictionary[field], list):
                        user_info[field].extend(field_dictionary[field])
                    else:
                        user_info[field].append(field_dictionary[field])
            users[username] = user_info
            # Write the updated data back to the file
            with open(credentials_file_path, "w") as file:
                json.dump(users, file, indent=4)
            print(f"Updated '{field_dictionary.keys}' to {username}'s info.")
            st.session_state['logged_username_info'] = users[username]
        else:
            print(f"User '{username}' not found.")
    except FileNotFoundError:
        print(f"File '{credentials_file_path}' not found.")