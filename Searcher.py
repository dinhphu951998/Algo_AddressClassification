from typing import Dict, Tuple, Optional

from IndexAnalyzer import Trie
from Autocorrect import autocorrect
from Utils import normalize_text_and_remove_accent

def search_locations_in_trie(tries: Dict[str, Trie], input_text: str, results) -> Tuple[Dict[str, Optional[str]], str]:
    matched_positions = set()

    remaining_chars = list(input_text)

    for category, reverse in [("province", True), ("district", False), ("ward", False)]:
        if results[category] != "":
            continue
        match = search_part(tries[category], input_text, matched_positions, remaining_chars, reverse)
        res = match[0]
        if match and res:
            input_text = input_text[:match[1]] + "," + input_text[match[2]:]
        results[category] = res
        print(input_text)
    # remaining_text = normalize_text_and_remove_accent(input_text)
    # for category, reverse in [("province", True), ("ward", False), ("district", False)]:
    #     if results[category] != "":
    #         continue
    #     match = search_part(tries[category], remaining_text, matched_positions, remaining_chars, reverse)
    #     res = match[0]
    #     if match and res:
    #         remaining_text = remaining_text[:match[1]] + "," + remaining_text[match[2]:]
    #         input_text = input_text[:match[1]] + "," + input_text[match[2]:]
    #     results[category] = res

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
        word = autocorrect(seg, trie, category)
        if word == "":
            continue
        segments.remove(seg)
        return word

    if reverse:
        segments.reverse()

    return ""

def search_part(trie, input_text, matched_positions, remaining_chars, reversed=False):
    it_range = range(len(input_text))
    matched_intervals = []
    if reversed:
        it_range = it_range.__reversed__()
    for i in it_range:
        if i in matched_positions:
            continue
        matches = trie.search_max_length(input_text, i)

        if matches:
            best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))  # Prioritize the end and length
            # Check if the best match is actually the longest match covering the end of the string
            if any(match[1] <= len(input_text) - 1 <= match[2] for match in matches):
                best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))
            print(best_match)
            # Ensure no overlap with previously matched regions
            start, end = best_match[1], best_match[2]
            if any(s <= start < e or s < end <= e for s, e in matched_intervals):
                continue  # Skip overlapping matches
            return best_match
    return "", None, None