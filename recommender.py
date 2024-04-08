import ast

from openai import OpenAI
client = OpenAI(api_key='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')


def get_video_prompt(user_info):
    prompt = f" \
                 please recommend a topic or a term for a video to be learned by the user based on the user’s information:\
                    Financial education level: {user_info['education_level']}\
                    Financial Interest Topic: {user_info['interest_topic']}\
                    Spending Behaviour: {user_info['spending_behavior']}\
                    current displayed videos: {user_info['present_videos']}\
                    Previously Watched and liked videos:{user_info['liked_video']}\
                    Previously Watched and disliked videos:{user_info['unliked_video']}\
                    Previously answered quiz questions successfully:{user_info['right_questions']}\
                    Previously answered quiz questions unsuccessfully:{user_info['wrong_questions']}\
                    Please provide only the topic and a description for the video in to 2 sentences:\
                    1-sentence of motivation to learn why to learn the topic:\
                    1-sentence of explanation for the user why you chose this topic for him.\
                    The format should be (please don't add any additional words):\
                    (“topic”, “motivation and explanation”)\
                    "
    return prompt

def get_new_video(user_info):

    prompt = get_video_prompt(user_info)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial guide in an web app"},
            {"role": "user", "content": prompt}
        ]
    )
    print(response)
    return response.choices[0].message.content


def get_question_prompt(user_info):
    prompt = f""" \
                    please recommend a question on a topics or a terms for a quiz to be answered by the user based on\
                    the user’s information, please don't repeat previously asked question:\
                    Financial education level: {user_info['education_level']}\
                    Financial Interest Topic: {user_info['interest_topic']}\
                    Spending Behaviour: {user_info['spending_behavior']}\
                    current displayed videos: {user_info['present_videos']}\
                    Previously Watched and liked videos:{user_info['liked_video']}\
                    Previously Watched and disliked videos:{user_info['unliked_video']}\
                    current displayed questions: {user_info['present_questions']}\
                    Previously answered quiz questions successfully:{user_info['right_questions']}\
                    Previously answered quiz questions unsuccessfully:{user_info['wrong_questions']}\
                    Please provide the question in the following format without any additional text:\
                    A dictionary that represent the question and it’s answers,\
                    like the following example, so I can later use question = json.loads(correct_json_str):           
        {{
            "question": "What is compound interest?",
            "options": [
                "Interest calculated on the initial principal only",
                "Interest calculated on the initial principal and all accumulated interest",
                "A fixed interest rate for the life of an investment",
                "Interest that compounds annually only"
            ],
            "answer": "Interest calculated on the initial principal and all accumulated interest",
            "explanation": "Compound interest is the interest on a loan or deposit calculated based on both the initial 
            principal and the accumulated interest from previous periods. It allows for the growth of an investment or 
            loan to accelerate over time, as interest is earned on top of interest, leading to significantly larger 
            amounts than simple interest, which is calculated only on the principal amount.
        }}"""

    return prompt


def get_new_question(user_info):

    prompt = get_question_prompt(user_info)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial guide in an web app"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def get_relevant_news_prompt(user_info, news_titles):
    prompt = f""" \
                    please leave the news titles relevant to the user based on the user’s information, take into 
                    consideration his level, what he likes. Leave those who you think he likes and those you think he may learn from:\
                    Financial education level: {user_info['education_level']}\
                    Financial Interest Topic: {user_info['interest_topic']}\
                    Spending Behaviour: {user_info['spending_behavior']}\
                    current displayed videos: {user_info['present_videos']}\
                    Previously Watched and liked videos:{user_info['liked_video']}\
                    Previously Watched and disliked videos:{user_info['unliked_video']}\
                    new titles: {news_titles}\
                    please return a list of ones and zeros at the length of the titles list. one if relevant news and 
                    zero otherwise. please provide only the list without any additional words"""

    return prompt


def get_relevant_news(user_info, news_titles):
    prompt = get_relevant_news_prompt(user_info, news_titles)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial guide in an web app"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content