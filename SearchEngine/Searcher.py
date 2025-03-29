from typing import Dict, Tuple, Optional

from IndexAnalyzer.IndexAnalyzer import Trie
from SearchEngine.Autocorrect import autocorrect
from Utils.Utils import normalize_text_but_keep_vietnamese, segment_text


def search_locations(tries: Dict[str, Trie], input_text: str) -> Tuple[Dict[str, Optional[str]], str]:
    """Searches the text using Tries and removes matched words."""
    results = {"ward": "", "district": "", "province": ""}
    matched_positions = set()

    input_text = normalize_text_but_keep_vietnamese(input_text)
    segments = segment_text(input_text)

    remaining_chars = list(input_text)

    for category in ["province", "ward", "district"]:
        trie = tries.get(category, None)

        if not trie:
            continue

        if category == "province":
            province = search_part(trie, input_text, matched_positions, remaining_chars, True)
            results["province"] = province if province else search_in_segment(segments, trie, "province", True)

        if category == "ward":
            ward = search_part(trie, input_text, matched_positions, remaining_chars)
            results["ward"] = ward if ward else search_in_segment(segments, trie, "ward")

        if category == "district":
            district = search_part(trie, input_text, matched_positions, remaining_chars)
            results["district"] = district if district else search_in_segment(segments, trie, "district")

    normalized_remaining_text = "".join(remaining_chars).strip()
    return results, normalized_remaining_text

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
        if match and match[1] not in matched_positions and match[2] - 1 not in matched_positions:
            matched_positions.update(range(match[1], match[2]))
            for j in range(match[1], match[2]):
                remaining_chars[j] = ""
            return match[0] # normalized result
    return ""

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