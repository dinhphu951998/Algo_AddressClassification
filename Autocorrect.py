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
from functools import lru_cache
import editdistance

from IndexAnalyzer import Trie
from Utils import normalize_text_but_keep_vietnamese_alphabet, normalize_text_but_keep_accent

# Define category ranking
CATEGORY_PRIORITY = {"province": 1, "district": 2, "ward": 3}  # Lower number = higher priority
COSINE_SIMILARITY_THRESHOLD = 0.7225  # If similarity < 0.7, return "null", the less value - the less strict
MAX_VALID_EDIT_DISTANCE = 3
COSINE_SIMILARITY_THRESHOLD_NUM = 0.85

# Damerau-Levenshtein Distance with max_distance
# def damerau_levenshtein(s1, s2, max_distance=3):
#     len_s1, len_s2 = len(s1), len(s2)
#     if abs(len_s1 - len_s2) > max_distance:
#         return max_distance + 1
#
#     prev_row = list(range(len_s2 + 1))
#     curr_row = [0] * (len_s2 + 1)
#
#     for i in range(1, len_s1 + 1):
#         curr_row[0] = i
#         min_row_value = i
#
#         for j in range(1, len_s2 + 1):
#             cost = 0 if s1[i - 1] == s2[j - 1] else 1
#             curr_row[j] = min(curr_row[j - 1] + 1, prev_row[j] + 1, prev_row[j - 1] + cost)
#             if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
#                 curr_row[j] = min(curr_row[j], prev_row[j - 2] + 1)
#
#             min_row_value = min(min_row_value, curr_row[j])
#
#         if min_row_value > max_distance:
#             return max_distance + 1
#
#         prev_row, curr_row = curr_row, prev_row
#
#     return prev_row[len_s2]

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
    print(category)
    for candidate_normalized in trie.all_words:
        distance = editdistance.distance(word_normalized, candidate_normalized)
        # Prioritize lower edit distance & higher-ranked category (Province > District > Ward)
        # if distance < min(best_distance, MAX_VALID_EDIT_DISTANCE):
        #     matches = [candidate_normalized]
        #     best_distance = distance
        # elif distance == min(best_distance, MAX_VALID_EDIT_DISTANCE):
        #     matches.append(candidate_normalized)
        if distance < MAX_VALID_EDIT_DISTANCE:
            matches.append(candidate_normalized)
            print(distance, candidate_normalized)
    # Check Cosine Similarity Threshold
    best_match = ""
    best_similarity = 0
    for match in matches:
        p = cosine_similarity(word_normalized, match)
        print(match, p)
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
