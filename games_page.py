import ast
import json
import time

import streamlit as st
import recommender
from utils import load_user_info, update_fields_in_user_info, search_youtube


def add_present_question(user_name):
    user_info = load_user_info(user_name)
    response = recommender.get_new_question(user_info)
    question_dict = json.loads(response)
    update_fields_in_user_info(user_name, {"present_questions": [question_dict]})


def update_user_info_after_quiz(username, updated_user_info):
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


def restart_quiz(user_name, num_present_questions):
    user_info = load_user_info(user_name)
    questions = user_info['present_questions']
    answers_result = st.session_state['answers_result']
    print("final", answers_result)
    for answer, question in zip(answers_result, questions):
        if answer:
            user_info['right_questions'].append(question['question'])
        else:
            user_info['wrong_questions'].append(question['question'])
    user_info['present_questions'] = []
    update_user_info_after_quiz(user_name, user_info)
    st.session_state['current_question'] = 0
    st.session_state['score'] = 0
    st.session_state['answers_result'] = [0 for i in range(num_present_questions)]


def show_financial_quiz():
    # st.header("Financial Quiz: Test Your Knowledge")
    # st.write("Test Your Knowledge")
    # st.write("---")
    username = st.session_state['logged_username']
    user_info = load_user_info(username)
    num_present_questions = 3

    if 'present_questions' not in user_info:
        update_fields_in_user_info(username, {'present_questions': [],
                                              'right_questions': [],
                                              'wrong_questions': []})
        user_info = load_user_info(username)

    while len(user_info['present_questions']) < num_present_questions:
        print("len in small")
        add_present_question(username)
        user_info = load_user_info(username)

    user_info = load_user_info(username)
    questions = user_info['present_questions']

    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0
        st.session_state['score'] = 0
        st.session_state['answers_result'] = [0 for i in range(num_present_questions)]

    if st.session_state['current_question'] >= len(questions):
        # Quiz is complete
        st.write(f"Quiz complete! Your score: {st.session_state['score']} / {len(questions)}")
        if st.button("Restart Quiz"):
            restart_quiz(username, num_present_questions)
            st.rerun()
        return  # Important to return here to avoid proceeding with the rest of the function

        # Proceed with showing questions if the quiz is not complete
    current_question = questions[st.session_state['current_question']]


    options = current_question["options"]

    _, options_col, _ = st.columns((1,4,1))
    with options_col:
        st.subheader(current_question["question"])
        for i, option in enumerate(options):
            if st.button(option, key=f"question_{st.session_state['current_question']}_option_{i}"):
                if option == current_question["answer"]:
                    st.session_state['score'] += 1
                    st.session_state['answers_result'][st.session_state['current_question']] = 1
                    st.success("Correct!")
                else:
                    st.error("Wrong answer.")
                time.sleep(1)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Answer", key=f"Show_answer_{st.session_state['current_question']}"):
            information = f"The correct answer is:<br>{current_question['answer']}<br><br>" \
                          f"why?<br>{current_question['explanation']}"
            st.markdown(information, unsafe_allow_html=True)

    with col2:
        if st.button("Deep Dive", key=f"deep_dive_{st.session_state['current_question']}"):
            video_link, image_link, title = search_youtube(current_question["question"])
            st.write(title)
            st.image(image_link)
    with col3:
        if st.button("Next", key=f"Next_{st.session_state['current_question']}"):
            st.session_state['current_question'] += 1
            st.rerun()

