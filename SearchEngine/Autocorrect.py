# Both Normalized and Un-normalized words are loaded to Trie
# Inputs are misspelled words (misspelled_words)
# Outputs are corrected words via Database
# If Output is 'null', please check Database if it really exists
# Two parameters can be tuned: COSINE_SIMILARITY_THRESHOLD = 0.75
#                                     distance = damerau_levenshtein(word_normalized, candidate_normalized, max_distance=3)
# Search Priority is set as province > district > ward

####################################################################
import unicodedata
import time
from collections import deque, Counter
import math

from IndexAnalyzer.IndexAnalyzer import Trie
from Utils.Utils import normalize_text_but_keep_vietnamese

# Start execution timer
start_time = time.perf_counter()

# Define category ranking
CATEGORY_PRIORITY = {"province": 1, "district": 2, "ward": 3}  # Lower number = higher priority
COSINE_SIMILARITY_THRESHOLD = 0.75  # If similarity < 0.7, return "null", the less value - the less strict

#
# class TrieNode:
#     def __init__(self):
#         self.children = {}
#         self.is_end_of_word = False
#         self.original_words = []  # Store multiple unnormalized words
#         self.category = None  # Province, District, Ward
#
#
# class Trie:
#     def __init__(self):
#         self.root = TrieNode()
#
#     def insert(self, word, category):
#         """Insert both normalized and unnormalized versions of the word."""
#         normalized_word = normalize_text(word)
#         node = self.root
#
#         for char in normalized_word:
#             if char not in node.children:
#                 node.children[char] = TrieNode()
#             node = node.children[char]
#         node.is_end_of_word = True
#         node.category = category
#
#         if word not in node.original_words:
#             node.original_words.append(word)
#
#     def get_all_words(self):
#         """Retrieve all words in the Trie along with their categories."""
#         words = []
#         queue = deque([(self.root, "")])
#
#         while queue:
#             node, curr_word = queue.popleft()
#             if node.is_end_of_word:
#                 for original_word in node.original_words:
#                     words.append((original_word, node.category))
#             for char, child in node.children.items():
#                 queue.append((child, curr_word + char))
#
#         return words

# Normalize text: Lowercase + Remove accents + Remore Spaces
# def normalize_text(text):
#     return unicodedata.normalize('NFKD', text.lower().strip()).encode('ASCII', 'ignore').decode('utf-8').replace(" ","")

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

# Optimized File Loading
# def load_words_from_file(file_path, category):
#     with open(file_path, "r", encoding="utf-8") as file:
#         return [(line.strip(), category) for line in file if line.strip() and not line.strip().isnumeric()]

# Initialize Trie and load words from files
# trie = Trie()
# file_paths = {
#     "District": "/Users/Klein/Desktop/IMP_Advanced_Algorithm/district_list.txt",
#     "Province": "/Users/Klein/Desktop/IMP_Advanced_Algorithm/province_list.txt",
#     "Ward": "/Users/Klein/Desktop/IMP_Advanced_Algorithm/ward_list.txt"
# }
#
# for category, file_path in file_paths.items():
#     for word, category in load_words_from_file(file_path, category):
#         trie.insert(word, category)

################################################# Vietnamese Typo Test Cases ###########################################
# misspelled_words = [
#     "hochjminh", "hnoi", "tanbin", "yensôn", "hòchĩmin",
#     "hoangmay", "cntho", "haiphongg", "dalat", "nhhatrang",
#     "quangngai", "dongnai", "phutho", "bacgang", "vinhlon",
#     "daklak", "bacleiu", "binhduong", "camphaa", "longxyuen",
#     "mitho", "kiengiangg", "thhuduc", "quangnamm", "vinhyen",
#     "thaingyen", "thanhhou", "dongthqp", "bacnin", "laocai",
#     "hajgiang", "namdin", "quangtri", "tiengiangg", "taynin",
#     "angang", "quangbinhh", "soctrang", "dienbeinn", "camu",
#     "binhthuann", "daklack", "danagn", "yenbbi", "backan",
#     "sonlaa", "thaibink", "binhphuocc", "binhdinhh", "travin",
#     "longan", "kontum", "gialaii", "hating", "quangninhh",
#     "dongnay", "lamdongg", "quangngai", "binhduon", "kiengiang",
#     "ninhbink", "phuyenn", "binh thuann", "tuyenquang", "vinhphuck",
#     "caamau", "daknongg", "haugiangg", "quangtrii", "quang nammm",
#     "tayninhh", "canthoo", "phuutho", "hungyenn", "barria",
#     "hoabinhh", "ngheanm", "quangbinhh", "quangngaii", "daklack",
#     "vinhlongg", "baclieuu", "thanhhoa", "binhdinhh", "thainguyenn",
#     "angiangg", "dongna4i", "dongthapp", "thuathienhu3e", "bacgang",
#     "ninhthuan", "phuyenn", "tiengianng", "quangninhh", "langsonn",
#     "longann", "binhthuann", "daknong", "hanamm", "qu3ang trii",
#     "wangnngai", "kantho", "tuyềnquae1ng", "taynin5hh", "thanhhóa",
#     "NinhP5hước", "YênK6Bái", "duongmin7hchau", "cẩmbinh", "sonl",
#     "tttrangdai", "tohiieu", "TieGiang", "hồ6chiminh"
# ]
#
# # Perform autocorrection
# corrected_results = [autocorrect(word, trie) for word in misspelled_words]
#
# # Print results
# for i in range(len(misspelled_words)):
#     category, corrected_word = corrected_results[i]
#     print(f'{misspelled_words[i]} -> "{category}": "{corrected_word}"')
#
# # End execution timer
# end_time = time.perf_counter()
# print(f"\nExecution time: {end_time - start_time:.4f} seconds")
