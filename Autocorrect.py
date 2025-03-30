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

from IndexAnalyzer import Trie
from Utils import normalize_text_but_keep_vietnamese

# Define category ranking
CATEGORY_PRIORITY = {"province": 1, "district": 2, "ward": 3}  # Lower number = higher priority
COSINE_SIMILARITY_THRESHOLD = 0.75  # If similarity < 0.7, return "null", the less value - the less strict

# Damerau-Levenshtein Distance with max_distance
def damerau_levenshtein(s1, s2, max_distance=3):
    len_s1, len_s2 = len(s1), len(s2)
    if abs(len_s1 - len_s2) > max_distance:
        return max_distance + 1

    prev_row = list(range(len_s2 + 1))
    curr_row = [0] * (len_s2 + 1)

    for i in range(1, len_s1 + 1):
        curr_row[0] = i
        min_row_value = i

        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr_row[j] = min(curr_row[j - 1] + 1, prev_row[j] + 1, prev_row[j - 1] + cost)
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                curr_row[j] = min(curr_row[j], prev_row[j - 2] + 1)

            min_row_value = min(min_row_value, curr_row[j])

        if min_row_value > max_distance:
            return max_distance + 1

        prev_row, curr_row = curr_row, prev_row

    return prev_row[len_s2]

# Cosine Similarity Function
def cosine_similarity(s1, s2):
    vec1, vec2 = Counter(s1), Counter(s2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[x] * vec2[x] for x in intersection)
    magnitude1 = math.sqrt(sum(vec1[x] ** 2 for x in vec1.keys()))
    magnitude2 = math.sqrt(sum(vec2[x] ** 2 for x in vec2.keys()))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0.0

# Autocorrection with Category Priority, Damerau-Levenshtein Distance & Cosine Similarity Check
def autocorrect(word, trie: Trie, category):
    all_words = trie.get_all_words()
    word_normalized = normalize_text_but_keep_vietnamese(word)
    best_match, best_distance, best_category = None, float("inf"), None

    for candidate in all_words:
        candidate_normalized = normalize_text_but_keep_vietnamese(candidate)
        distance = damerau_levenshtein(word_normalized, candidate_normalized, max_distance=3)

        # Prioritize lower edit distance & higher-ranked category (Province > District > Ward)
        if (distance < best_distance) or (
                distance == best_distance and CATEGORY_PRIORITY[category] < CATEGORY_PRIORITY[best_category]):
            best_distance, best_match, best_category = distance, candidate, category

    # Check Cosine Similarity Threshold
    if best_match and cosine_similarity(word_normalized, normalize_text_but_keep_vietnamese(best_match)) < COSINE_SIMILARITY_THRESHOLD:
        return ("null", "")
    return (best_category, best_match) if best_match else ("Unknown", word)
