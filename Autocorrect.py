# Both Normalized and Un-normalized words are loaded to Trie
# Inputs are misspelled words (misspelled_words)
# Outputs are corrected words via Database
# If Output is 'null', please check Database if it really exists
# Two parameters can be tuned: COSINE_SIMILARITY_THRESHOLD = 0.75
#                                     distance = damerau_levenshtein(word_normalized, candidate_normalized, max_distance=3)
# Search Priority is set as province > district > ward

####################################################################
import time
from collections import Counter
import math

import editdistance

from IndexAnalyzer import Trie

# Define category ranking
CATEGORY_PRIORITY = {"province": 1, "district": 2, "ward": 3}  # Lower number = higher priority
COSINE_SIMILARITY_THRESHOLD = 0.73  # If similarity < 0.7, return "null", the less value - the less strict
MAX_VALID_EDIT_DISTANCE = 3
COSINE_SIMILARITY_THRESHOLD_NUM = 0.85

# Cosine Similarity Function
def cosine_similarity(s1, s2):
    vec1, vec2 = Counter(s1), Counter(s2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[x] * vec2[x] for x in intersection)
    magnitude1 = math.sqrt(sum(vec1[x] ** 2 for x in vec1.keys()))
    magnitude2 = math.sqrt(sum(vec2[x] ** 2 for x in vec2.keys()))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0.0

# Autocorrection with Category Priority, Damerau-Levenshtein Distance & Cosine Similarity Check
def autocorrect(word_normalized, trie: Trie, category):
    best_distance = float("inf")
    matches = []
    for candidate_normalized in trie.all_words:
        distance = editdistance.distance(word_normalized, candidate_normalized)

        # Prioritize lower edit distance & higher-ranked category (Province > District > Ward)
        if distance < min(best_distance, MAX_VALID_EDIT_DISTANCE):
            matches = [candidate_normalized]
            best_distance = distance
        elif distance == min(best_distance, MAX_VALID_EDIT_DISTANCE):
            matches.append(candidate_normalized)

    # Check Cosine Similarity Threshold
    best_match = ""
    best_similarity = 0
    for match in matches:
        p = cosine_similarity(word_normalized, match)

        # Xác định ngưỡng phù hợp
        if any(char.isdigit() for char in word_normalized):
            threshold = COSINE_SIMILARITY_THRESHOLD_NUM
        else:
            threshold = COSINE_SIMILARITY_THRESHOLD

        # So sánh tương đồng
        if p > threshold and p > best_similarity:
            best_similarity = p
            best_match = match

    return best_match
