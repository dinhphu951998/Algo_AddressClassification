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
    print(text)
    unit_words = [
        "huyen",  # huyện
        "quan",  # quận
        "thanh pho",  # thành phố
        "tp",  # tp (abbreviation for thành phố)
        "tinh",  # tỉnh
        "xa",  # xã
        "phuong",  # phường
        "thi xa",  # thị xã
        "thi tran"
    ]

    for unit in unit_words:
        text = re.sub(r'\b' + re.escape(unit) + r'\b', '', text)

    # Optionally, remove extra spaces resulting from the removals.
    text = re.sub(r'\s+', ' ', text).strip()
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
