from typing import Dict, Tuple, Optional

from IndexAnalyzer import Trie
from Autocorrect import autocorrect


def search_locations_in_trie(tries: Dict[str, Trie], input_text: str, results) -> Tuple[Dict[str, Optional[str]], str]:
    matched_positions = set()

    remaining_chars = list(input_text)

    for category, reverse in [("province", True), ("ward", False), ("district", False)]:
        if results[category] != "":
            continue
        res, input_text = search_in_trie(tries[category], input_text, matched_positions, remaining_chars, reverse)
        results[category] = res

    return results, input_text

def search_locations_in_segments(tries: Dict[str, Trie], segments: [], results) -> Tuple[Dict[str, Optional[str]], str]:
    for category, reverse in [("province", True), ("ward", False), ("district", False)]:
        if results[category] != "":
            continue

        res = search_in_segment(segments, tries[category], category, reverse)
        results[category] = res

    return results, segments

def search_in_trie(trie, input_text, matched_positions, remaining_chars, reverse):
    match = search_part(trie, input_text, matched_positions, remaining_chars, reverse)
    res = match[0]
    if match and res:
        input_text = input_text[:match[1]] + "," + input_text[match[2]:]
    return res, input_text

def search_in_segment(segments, trie, category, reverse=False):
    if reverse:
        segments.reverse()

    for seg in segments:
        _, ward = autocorrect(seg, trie, category)
        if ward:
            segments.remove(seg)
            return ward

    if reverse:
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