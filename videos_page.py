import streamlit as st
from PIL import Image
import ast
import json

import recommender
from utils import search_youtube, load_user_info, update_fields_in_user_info


img_compounding_interest = Image.open("images/compound-interest.webp")
img_inflation = Image.open("images/inflation.jpg")
img_snp500 = Image.open("images/snp500.jpeg")


def update_user_info_by_feedback(username, updated_user_info):
    """Add a new field to an existing user's information in the JSON credentials file."""
    credentials_file_path = "credentials.json"
    try:
        # Load the existing users data
        with open(credentials_file_path, "r") as file:
            users = json.load(file)

        # Check if the user exists
        if username in users:
            users[username] = updated_user_info
            # Write the updated data back to the file
            with open(credentials_file_path, "w") as file:
                json.dump(users, file, indent=4)

            st.session_state['logged_username_info'] = users[username]
        else:
            print(f"User '{username}' not found.")
    except FileNotFoundError:
        print(f"File '{credentials_file_path}' not found.")


def handle_video_feedback(video_id, preference):
    """Handles user feedback for video recommendations and shows a new video as mockup feedback."""
    username = st.session_state["logged_username"]
    user_info = load_user_info(username)
    present_videos = user_info["present_videos"]

    for i in range(len(present_videos)):
        video = present_videos[i]
        if video['topic'] == video_id:
            removed_video = present_videos.pop(i)
            break

    if preference == "like":
        user_info["liked_video"].append(removed_video['topic'])
    else:
        user_info["unliked_video"].append(removed_video['topic'])
    user_info['present_videos'] = present_videos
    update_user_info_by_feedback(username, user_info)





def show_video_with_feedback(image_url, title, description, video_url):
    """Displays a video section with feedback options."""
    with st.container():
        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.image(image_url, caption=title)
        with text_column:
            st.subheader(title)
            st.write(description)
            st.markdown(f"[Watch Video...]({video_url})")


        col1, col2, _ = st.columns((1,1,6))
        with col1:
            if st.button("👍 Like", key=f"like_{title}"):
                st.session_state['feedback'] = 'like'
                st.session_state['feedback_received'] = True
        with col2:
            if st.button("👎 Dislike", key=f"dislike_{title}"):
                st.session_state['feedback'] = 'dislike'
                st.session_state['feedback_received'] = True

            # Now, check the session state for feedback outside the button checks
            if st.session_state['feedback_received']:
                # This print statement is for debugging; replace it with your actual feedback handling
                print(f"Feedback received: {st.session_state['feedback']}")
                handle_video_feedback(title, st.session_state['feedback'])
                # show_recommended_videos()
                st.session_state['feedback_received'] = True
                st.rerun()


def add_present_video(user_name):
    user_info = load_user_info(user_name)
    response = recommender.get_new_video(user_info)
    topic, description = ast.literal_eval(response)
    video_link, image_link, _ = search_youtube(topic)
    video_dict = {
        "topic": topic,
        "video_url": video_link,
        "description": description,
        "image_url": image_link
    }
    update_fields_in_user_info(user_name, {"present_videos": [video_dict]})


def present_video():
    videos = st.session_state['present_video']
    for video in videos:
        show_video_with_feedback(title=video["topic"],
                                 image_url=video['image_url'],
                                 description=video['description'],
                                 video_url=video['video_url'])


def show_recommended_videos():
    st.session_state['feedback_received'] = False
    # st.header("Recommended Videos")
    # st.write("Expand Your Knowledge")
    # st.write("---")
    num_presented_videos = 2
    user_name = st.session_state['logged_username']
    user_info = load_user_info(user_name)

    if 'present_videos' not in user_info:
        update_fields_in_user_info(user_name, {'present_videos': [],
                                               'liked_video': [],
                                               'unliked_video': []})
        user_info = load_user_info(user_name)


    while len(user_info['present_videos']) < num_presented_videos:
        print("len in small")
        add_present_video(user_name)
        user_info = load_user_info(user_name)

    st.session_state['present_video'] = user_info["present_videos"]

    present_video()
