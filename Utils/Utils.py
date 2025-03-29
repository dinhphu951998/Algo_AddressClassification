import re

import unicodedata

from Helper.VietnameseHelper import VietnameseHelper

helper = VietnameseHelper()

def normalize_text(text, remove_space=True):
    text = unicodedata.normalize('NFKD', text.lower().strip()).encode('ASCII', 'ignore').decode('utf-8')
    # text = helper.remove_vietnamese_signs(text).lower()
    if remove_space:
        text = text.replace(" ","")
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
