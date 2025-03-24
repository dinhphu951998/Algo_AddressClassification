import re
from Helper.VietnameseHelper import VietnameseHelper

helper = VietnameseHelper()

def normalize_text(text):
    text = text.lower()
    text = helper.remove_vietnamese_signs(text).lower()
    text = helper.remove_special_characters(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize_search_term_by_character(text):
    text = normalize_text(text)
    text = re.sub(r'\s+', '', text)
    tokens = list(text)
    return tokens


def tokenize_search_term(text):
    text = normalize_text(text)
    segments = [segment.strip() for segment in text.split(' ')]
    tokens = []
    for seg in segments:
        seg = seg.strip()
        tokens.append(seg)
    return tokens
