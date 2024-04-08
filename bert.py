from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from scipy.spatial.distance import cosine


def get_representation(sentence):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embedding = model.encode(sentence)
    return embedding


def find_closest_titles(query_vector, new_titles_vectors_dict, num_news):
    # Calculate cosine similarity between query vector and each title vector
    similarities = {}
    for title, vector in new_titles_vectors_dict.items():
        # Using 1 - cosine similarity to turn distance into similarity
        # Cosine returns distance, so subtract from 1 to get similarity
        similarity = 1 - cosine(query_vector, vector)
        similarities[title] = similarity

    # Sort titles by highest similarity
    sorted_titles = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

    # Return the top num_news titles (or all if less than num_news are available)
    closest_titles = [title for title, _ in sorted_titles[:num_news]]

    return closest_titles