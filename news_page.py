import ast

import streamlit as st
import feedparser
from utils import load_user_info

import recommender
import bert


def get_feed(url):
    return feedparser.parse(url)

def get_publish_date(published):
    words_list = published.split(" ")[:4]
    date = ""
    for word in words_list:
        date = date + word
        date = date + " "

    return date


def show():
    rss_url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362"
    feed = get_feed(rss_url)

    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

    count = 0
    num_articles = 30
    num_relevant = 5
    num_search = 2
    all_entries = []
    for entry in feed.entries:
        if 'summary' in entry:
            all_entries.append(entry)
    all_entries = all_entries[:num_articles]
    news_summaries = [entry.summary for entry in all_entries]
    news_titles = [entry.title for entry in all_entries]

    # recommender.create_audio_file(news_titles, news_summaries)
    # st.audio("news.mp3", format='audio/mp3')


    show_relevant_news = False
    if 'relevant_news' not in st.session_state and show_relevant_news:
        username = st.session_state['logged_username']
        user_info = load_user_info(username)
        list_str = recommender.get_relevant_news(user_info, news_summaries)
        st.session_state['relevant_news'] = ast.literal_eval(list_str)

    if 'news_titles_representation' not in st.session_state:
        st.session_state['news_titles_representation'] = {}
        progress_bar = st.progress(0)
        for i, entry in enumerate(all_entries):
            st.session_state['news_titles_representation'][entry] = bert.get_representation(entry.title)
            progress = (i + 1) / len(all_entries)
            progress_bar.progress(progress)
        progress_bar.progress(1.0)

    if 'closest_titles' not in st.session_state:
        st.session_state['closest_titles'] = None

    search_col, checkbox_col, _ = st.columns((1,1,2))
    with search_col:
        query = st.text_input('Search The News', key="search", placeholder="search")
    with checkbox_col:
        show_relevant_news = st.checkbox('Show Recommended News', value=False)

    if query:
        query_vector = bert.get_representation(query)
        st.session_state['closest_titles'] = bert.find_closest_titles(query_vector,
                                                                      st.session_state['news_titles_representation'],
                                                                      num_search)
    else:
        st.session_state['closest_titles'] = None

    if show_relevant_news:
        for is_relevant, entry in zip(st.session_state['relevant_news'], all_entries):
            if is_relevant and (st.session_state['closest_titles'] is None or
                                entry in st.session_state['closest_titles']):
                published = get_publish_date(entry.published)

                with st.expander(f"### {entry.title} - {published}"):
                    st.write(entry.summary)
                    st.markdown(f"[Read more]({entry.link})", unsafe_allow_html=True)

                count += 1
                if count >= num_relevant:
                    break
    else:
        for entry in all_entries:
            if st.session_state['closest_titles'] is None or entry in st.session_state['closest_titles']:
                published = get_publish_date(entry.published)

                with st.expander(f"### {entry.title} - {published}"):
                    st.write(entry.summary)
                    st.markdown(f"[Read more]({entry.link})", unsafe_allow_html=True)

                count += 1
                if count >= num_articles:
                    break
