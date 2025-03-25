from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from underthesea import word_tokenize
from fuzzywuzzy import process

class Solution:
    def __init__(self):
        self.province_path = '/content/province_list.txt'
        self.district_path = '/content/district_list.txt'
        self.ward_path = '/content/ward_list.txt'

        # Load province, district, and ward lists
        self.province_list = self.load_list(self.province_path)
        self.district_list = self.load_list(self.district_path)
        self.ward_list = self.load_list(self.ward_path)
        self.address_database = self.province_list + self.district_list + self.ward_list

        # Initialize TF-ISF matcher
        self.vectorizer = TfidfVectorizer()
        self.address_vectors = self.vectorizer.fit_transform(self.address_database)
    
    def load_list(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []

    def preprocess(self, s: str):
        """
        Preprocess input string by normalizing text and tokenizing.
        """
        s = s.lower()
        s = re.sub(r"[?/\\~.,]+", " ", s)  # Remove special characters
        s = word_tokenize(s, format="text")
        return s

    def match_using_tfidf(self, s: str):
        """
        Find the best match using TF-IDF similarity score.
        """
        input_vector = self.vectorizer.transform([s])
        similarity_scores = cosine_similarity(input_vector, self.address_vectors).flatten()
        best_match_idx = np.argmax(similarity_scores)
        return self.address_database[best_match_idx] if similarity_scores[best_match_idx] > 0.4 else ""

    def process(self, s: str):
        """
        Process the given address string to extract the best-matching address component.
        """
        s = self.preprocess(s)
        tfidf_match = self.match_using_tfidf(s)
        return {"normalized_address": tfidf_match}
