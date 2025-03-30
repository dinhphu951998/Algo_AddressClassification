from typing import Dict, Tuple, Optional

from IndexAnalyzer import Trie
from Autocorrect import autocorrect
from Utils import normalize_text_but_keep_vietnamese_alphabet, segment_text, normalize_text_but_keep_accent


def search_locations(tries: Dict[str, Trie], input_text: str) -> Tuple[Dict[str, Optional[str]], str]:
    """Searches the text using Tries and removes matched words."""
    results = {"ward": "", "district": "", "province": ""}
    matched_positions = set()

    segments = segment_text(input_text)
    input_text = normalize_text_but_keep_accent(",".join(segments))

    remaining_chars = list(input_text)

    for category, reversed in [("province", True), ("ward", False), ("district", False)]:
        trie = tries.get(category, None)
        if not trie:
            continue

        match = search_part(trie, input_text, matched_positions, remaining_chars, reversed)
        res = match[0]
        if match and res:
            input_text = input_text[:match[1]] + "," + input_text[match[2]:]
        results[category] = res

    segments = segment_text(input_text, False)
    for category, reversed in [("province", True), ("ward", False), ("district", False)]:
        trie = tries.get(category, None)
        if not trie:
            continue

        if results[category]:
            continue

        res = search_in_segment(segments, trie, category, reversed)
        results[category] = res

    return results, "normalized_remaining_text"

def search_in_segment(segments, trie, category, reversed=False):
    if reversed:
        segments.reverse()

    for seg in segments:
        _, ward = autocorrect(seg, trie, category)
        if ward:
            segments.remove(seg)
            return ward

    if reversed:
        segments.reverse()

    return ""

def search_part(trie, input_text, matched_positions, remaining_chars, reversed=False):
    it_range = range(len(input_text))
    if reversed:
        it_range = it_range.__reversed__()
    for i in it_range:
        if i in matched_positions:
            continue
        match = trie.search_max_length(input_text, i)
        if match:
            return match
    return "", None, None

# def search_part_reversed(trie, input_text, matched_positions, remaining_chars):
#     for i in range(len(input_text) - 1, -1, -1): # Reverse start at len - 1, end at -1 exclusive, step -1
#         if i in matched_positions:
#             continue
#         match = trie.search(input_text, i)
#         if match:
#             matched_positions.update(range(match[1], match[2]))
#             for j in range(match[1], match[2]):
#                 remaining_chars[j] = ""
#             return match[0] # normalized result
#     return ""